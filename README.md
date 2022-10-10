# Cxsign

## 功能介绍

超星学习通接口调用，支持登录、签到。

- 普通签到
- 照片签到（后续更新支持）
- 签到码签到
- 手势签到
- 位置签到

> 注意  
> 手势签到和二维码签到<font color="red">不需要</font>签到码  
> 二维码签到<font color="red">不被支持</font>

配置和日志文件通过web服务查看和修改。

**使用setup.py来初始化此项目，然后打开web服务器，通过 http://127.0.0.1:5000/ 来进行配置的修改。**

---

## config.json 说明

### xxt

- username:  学习通账号，最好填写手机号
- passwd：   学习通密码
- address：  位置签到时，显示的地址
- latitude： 位置签到时，地址的纬度
- longitude：位置签到时，地址的经度
- picname：  照片签到要使用的照片id

### pushplus

> 使用网站 [pushplus(推送加)](http://www.pushplus.plus/) 提供的免费一对一微信公众号消息推送服务

- token：pushplus你的专属token

---

## 部署教程

 - 1. 运行 setup.py 初始化根目录。
 - 2. 使用 `pip install -r requirements.txt` 安装依赖库。
 - 3. 运行 ./web/app.py 。
 - 4. 访问 http://127.0.0.1:5000/ 进行配置。
 - 5. 使用 crontab 定时运行 ./corn/main.py 即可实现自动签到。
 - 6. 想要在互联网上修改配置查看日志，把 web 服务配置到 wsgi 服务器上即可。