import xxt, pushplus, time, os.path, json, datetime

mainpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
confaddr = os.path.join(mainpath, 'config.json')
signlog = os.path.join(mainpath, 'log', 'autosign.log')
errorlog = os.path.join(mainpath, 'log', 'error.log')

with open(confaddr, encoding='utf-8') as f:
    conf = json.load(f)

def write_log(text):
    with open(signlog, 'a', encoding='utf-8') as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n'+text+'\n')

def write_err(text):
    with open(errorlog, 'a', encoding='utf-8') as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n'+text+'\n')

def auto_sign_in(a, sleep=30):
    while True:
        try:
            for i in a.subject:
                m = a.class_sign_in(i)
                if m:
                    for j in m:
                        write_log(j['签到模式']+' | '+('成功' if j['签到状态']==1 else '失败')+' | '+j['当前课程']+' | '+('空' if j['任务名称']=='' else j['任务名称']))
                        pushplus.push_wx(conf['pushplus']['token'], ('学习通签到成功' if j['签到状态']==1 else '学习通签到失败'), j)
        except Exception as err:
            errtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            write_err(str(err))
        time.sleep(sleep)
        end_time = datetime.datetime.now()
        if (end_time-start_time).seconds >= 15600:
            write_log('正常登出。')
            return True

start_time = datetime.datetime.now()
try:
    my = xxt.Cxsign(conf['xxt'])
    write_log('登陆成功！')
    ss = True
except Exception as err:
    write_log('登录失败：请查看错误日志。')
    write_err(str(err))
    ss = False
    
if ss:
    auto_sign_in(my)
