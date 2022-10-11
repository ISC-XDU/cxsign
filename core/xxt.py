import requests, json, time, os.path
from fake_useragent import UserAgent

type_name = {2: '签到', 4: '抢答', 5: '主题讨论', 11: '选人', 42: '随堂练习',
             45: '通知', 56: '超星课堂', 64: '腾讯会议'}
url = {'login': 'https://passport2-api.chaoxing.com/v11/loginregister',
        'get_subject': "http://mooc1-api.chaoxing.com/mycourse/backclazzdata",
        'get_active_list': 'https://mobilelearn.chaoxing.com/v2/apis/active/student/activelist',
        'get_active_info': 'https://mobilelearn.chaoxing.com/v2/apis/active/getPPTActiveInfo',
        'get_attend_info': 'https://mobilelearn.chaoxing.com/v2/apis/sign/getAttendInfo',
        'sign_in': 'https://mobilelearn.chaoxing.com/v2/apis/sign/signIn',
        'pre_sign': 'https://mobilelearn.chaoxing.com/newsign/preSign',
        'location_sign_in': 'https://mobilelearn.chaoxing.com/pptSign/stuSignajax',
        'get_sign_list': 'https://mobilelearn.chaoxing.com/v2/apis/signStat/getActiveList'}
#headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 11; RMX1971 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.61 Mobile Safari/537.36 (device:RMX1971) Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_5.3.1_android_phone_861_83 (@Kalimdor)_c1be83e0ce524650a9132fed7b3f32cd'}
headers = {'User-Agent': UserAgent().chrome}

class Cxsign:
    def __init__(self, conf):
        self.__user = {'uname': conf['username'], 'code': conf['passwd']}
        self.conf = conf
        self.subject = []
        self.processed_sign = []

        login = self.__login()
        if login['status']:
            self.__get_subject()
        else:
            raise Exception(login['mes'])

    def __login(self):
        self.session = requests.session()
        res = self.session.post(url=url['login'], data=self.__user, headers=headers)
        return json.loads(res.text)

    def __get_subject(self):
        res = self.session.get(url['get_subject'], headers=headers)
        cdata = json.loads(res.text)
        if (cdata['result'] != 1):
            print("课程列表获取失败")
        else:
            for i in cdata['channelList']:
                if 'cpi' in i:
                    self.__cpi = i['cpi']
                    break
            for i in cdata['channelList']:
                if ("course" not in i['content']):
                    continue
                self.subject.append([i['content']['id'], i['content']['course']['data'][0]['name'], i['content']['course']['data'][0]['id']])

    #input:课程信息数组
    #output:签到活动列表
    #error:False 未获取到活动列表
    def get_sign_list(self, l):
        data = {'classId': l[0], 'courseId':l[2],"page":1,"pageSize":1000}
        res = self.session.get(url['get_sign_list'], headers=headers, params=data)
        cdata = json.loads(res.text)
        if cdata['result']==1:
            return cdata['data']['list']
        else:
            return False

    #input:课程信息数组
    #output:所有活动列表
    #error:!应补充一个获取失败
    def get_active_list(self, i):
        data = {'fid': '3043', 'courseId': i[2], 'classId': i[0], 'showNotStartedActive': '0'}
        res = self.session.get(url['get_active_list'], params=data, headers=headers)
        cdata = json.loads(res.text)
        return cdata['data']['activeList']

    #input:活动id
    #output:签到活动具体信息列表
    #error:
    def get_info(self, i):
        result = []
        data = {'activeId': i}
        res = self.session.get(url['get_attend_info'], params=data, headers=headers)
        result.append(json.loads(res.text)['data']['status'])
        res = self.session.get(url['get_active_info'], params=data, headers=headers)
        m = json.loads(res.text)['data']
        result.extend([m['otherId'], m['ifphoto']])
        return result

    #input:活动id
    #output:签到成功True失败False
    #error:
    def normal_sign_in(self, i):
        data = {'activeId': i}
        res = self.session.get(url['sign_in'], params=data, headers=headers)
        if json.loads(res.text)['result']==1:
            return True
        else:
            return False

    #input:活动id
    #output:签到成功True失败False
    #error:
    def location_sign_in(self, i):
        data = {'activePrimaryId': i}
        self.session.get(url['pre_sign'], params=data, headers=headers)
        data = {'address': self.conf['address'], 'activeId': i, 'latitude': self.conf['latitude'], 'longitude':self.conf['longitude']}
        res = self.session.get(url['location_sign_in'], params=data, headers=headers)
        if res.text=='success':
            return True
        else:
            return False

    #input:活动id
    #output:签到动作结果字典
    #error:
    def sign_in(self, i):
        sign_in_type = {0: '普通签到', 2: '二维码签到', 3: '手势签到', 4: '位置签到', 5: '签到码签到'}
        m = self.get_info(i)
        if m[2]:
            sign_in_type[0] = '图片签到'
        if m[0]==1:
            return {'status': 1, 'reason': '已经签到', 'type': sign_in_type[m[1]]}
        else:
            if (m[1] in [3,5]) or (m[1]==0 and m[2]==0):
                if self.normal_sign_in(i):
                    return {'status': 1, 'reason': '签到成功', 'type': sign_in_type[m[1]]}
            elif m[1]==4:
                if self.location_sign_in(i):
                    return {'status': 1, 'reason': '签到成功', 'type': sign_in_type[m[1]]}
            else:
                return {'status': 0, 'reason': '不支持此签到模式', 'type': sign_in_type[m[1]]}
            return {'status': 0, 'reason': '未知原因', 'type': sign_in_type[m[1]]}

    #input:课程信息数组
    #output:签到结果列表
    #error:False 未获取到活动列表
    def class_sign_in(self, i):
        result = []
        a = self.get_sign_list(i)
        if a:
            for j in a:
                if j['activeType']==2 and j['status']==1 and j['activeid'] not in self.processed_sign:
                    if self.get_info(j['activeid'])[0]==1:
                        self.processed_sign.append(j['activeid'])
                    else:
                        m = self.sign_in(j['activeid'])
                        self.processed_sign.append(j['activeid'])
                        push_data = {'签到状态': m['status'], '当前课程': i[1],'任务名称': j['name'], '签到模式': m['type'],
                                     '签到说明': m['reason'], '发起时间': j['starttime']}
                        result.append(push_data)
            return result
        else:
            return False
