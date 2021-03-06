#!/usr/bin/env python
# coding: utf-8



import requests
import base64
import re
import datetime
from retry import retry







class CX:
    # 实例化请传入手机号和密码
    @retry(tries=4)
    def __init__(self, phonenums, password,seatNum):
        self.acc = phonenums 
        self.pwd = password
        self.result=''
        self.mappid = None
        self.incode = None
        self.deptIdEnc = '991fe2698ebc49b9'
        self.room = None
        self.deptId = None
        self.db = {
            'sb': 0,
            'nb': 0
        }
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11' ,
        }
        self.login()

        self.submit('866', seatNum)

    # 获取cookies 
    def login(self):
        c_url = 'https://passport2.chaoxing.com/mlogin?loginType=1&newversion=true&fid=&refer=http%3A%2F%2Foffice.chaoxing.com%2Ffront%2Fthird%2Fapps%2Fseat%2Findex'
        self.session.get(c_url).cookies.get_dict()
        data = {
            'fid': '-1',
            'uname': self.acc,
            'password': self.pwd,
            'Referer': 'https://office.chaoxing.com/',
            't': 'true',
            "verify": "0"
        }

        self.session.post('https://passport2.chaoxing.com/fanyalogin', data=data)
        s_url = 'https://office.chaoxing.com/front/third/apps/seat/index'
        self.session.get(s_url)

    # 标准时间转换
    # 预约座位 需要自己修改
    def submit(self,roomId,seatNum):
        # 注意 老版本的系统需要将url中的seat改为seatengine且不需要第一步获取list。有可能需要提供seatId的值
        # 获取token
        tomorrow = (datetime.datetime.now()+datetime.timedelta(1)).strftime('%Y-%m-%d')
        # tomorrow = (datetime.datetime.now()).strftime('%Y-%m-%d')
        response = self.session.get(url='https://office.chaoxing.com/front/apps/seatengine/select?seatId=602&'
                                    f'id={roomId}&'          # 房间id roomId 可以从self.room_id_name获取 请自行发挥
                                    f'day={tomorrow}&'   # 预约时间 上下需保持一致
                                    'backLevel=2&'.format(roomId)  )    # 必须的参数2)
        token = re.compile("token: '(.*)'").findall(response.text)[0]
        
        response = self.session.get(url='https://office.chaoxing.com/data/apps/seatengine/submit?seatId=602&'
                                    f'roomId={roomId}&'      # 房间id roomId 上下需保持一致
                                    'seatId=602&'
                                    'startTime=8%3A30&' # 开始时间%3A代表: 自行替换9（小时）和后面00（分钟） 必须
                                    'endTime=23%3A00&'  # 结束时间 规则同上
                                    f'day={tomorrow}&'   # 预约时间 上下需保持一致
                                    f'seatNum={seatNum}&'      # 座位数字 与桌上贴纸一致
                                    f'token={token}')
        
        seat_result = response.json()
        self.result = seat_result
def send_message(msg):
    title = msg['msg']
    content = msg['success']
    api = 'https://sctapi.ftqq.com/SCT147683TbA8CuXrSgiIaPQO7EcyNxdvt.send?'
    data = {
        'text':title,
        'desp':content
    }
    requests.post(api,data=data)

cx = CX('13007491638','QGxpdmlvbGV0MDczMQ==','200')
send_message(cx.result)





