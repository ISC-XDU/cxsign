import json, os.path
from flask import Flask,render_template,url_for, request, session, redirect

mainpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
confaddr = os.path.join(mainpath, 'config.json')
confbackup = os.path.join(mainpath, 'config_backup.json')
signlog = os.path.join(mainpath, 'log', 'autosign.log')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'helloww'

@app.route('/', methods=['GET', 'POST'])
def index():
    with open(confaddr, 'rt', encoding='utf-8') as f:
        conf = json.load(f)
    if session.get('check')==1:
        return render_template('change.html', dict1=conf)
    elif request.form.get('pass')=='pass':
        session['check'] = 1
        return redirect(url_for('index'))
    else:
        return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    if session.get('check')==1:
        typ = request.form.get('type')
        if typ in ['xxt', 'email', 'pushplus']:
            with open(confaddr, 'rt', encoding='utf-8') as f:
                conf = json.load(f)
            with open(confbackup, 'rt', encoding='utf-8') as f:
                conf_bu = json.load(f)
            for i,j in conf[typ].items():
                req = request.form.get(i)
                if req not in ['', '<--'] and i in ['latitude', 'longitude']:
                    req = float(req)
                if req=='<--':
                    a = conf[typ][i]
                    conf[typ][i] = conf_bu[typ][i]
                    conf_bu[typ][i] = a
                elif req!='' and req!=j:
                    conf_bu[typ][i] = conf[typ][i]
                    conf[typ][i] = req
            with open(confbackup, 'wt', encoding='utf-8') as f:
                f.write(json.dumps(conf_bu, ensure_ascii=False))
            with open(confaddr, 'wt', encoding='utf-8') as f:
                f.write(json.dumps(conf, ensure_ascii=False))
            return redirect(url_for('index'))
        else:
            return '非法的参数'
    return redirect(url_for('index'))

@app.route('/log')
def log():
    with open(signlog, 'rt', encoding='utf-8') as f:
        res = f.read()
    l = res.split('\n')
    return render_template('log.html', l=l)

if __name__=='__main__':
    app.run()
