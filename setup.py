import os, json

mainpath = os.path.dirname(os.path.abspath(__file__))

conf = {'xxt'       :   {'username' : '',
                        'passwd'    : '',
                        'address'   : '',
                        'latitude'  : '',
                        'longitude' : '',
                        'picname'   : ''},
        'pushplus'  :   {'token'    : ''}}

def initdir(name):
    if os.path.isfile(os.path.join(mainpath, name)):
        print('程序根目录下存在文件{}，请删除后重试。'.format(name))
        return False
    elif not os.path.exists(os.path.join(mainpath, name)):
        os.mkdir(os.path.join(mainpath, name))
    return True

def loadconf(name):
    with open(os.path.join(mainpath, name), 'wt', encoding='utf-8') as f:
        f.write(json.dumps(conf, ensure_ascii=False))

def initconf(config='config.json', backup='config_backup.json'):
    if os.path.isfile(os.path.join(mainpath, config)):
        if os.path.isfile(os.path.join(mainpath, backup)):
            return True
    else:
        loadconf(config)
    loadconf(backup)
    return True

if __name__=='__main__':
    if initdir('log') and initconf():
        print('初始化完成！')
    else:
        print('初始化失败！')
