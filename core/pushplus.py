import requests, json, os.path

url = 'http://www.pushplus.plus/send'
error = { 200: '执行成功',
          302: '未登录',
          401: '请求未授权',
          403: '请求IP未授权',
          500: '系统异常，请稍后再试',
          600: '数据异常，操作失败',
          805: '无权查看',
          888: '积分不足，需要充值',
          900: '用户账号使用受限',
          999: '服务端验证错误' }

def push_wx(token, title, content):
    data = {'token': token, 'title': title, 'content': content, 'template': 'json'}
    count = 2
    while count>0:
        count -= 1
        res = requests.post(url, json=data)
        res = json.loads(res.text)
        if res['code']==200:
            return True
        elif res['code'] in [500, 600, 999]:
            continue
        else:
            return False
    return False
