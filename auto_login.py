import httplib
import urllib

login_data = {"deviceId": "865863024697364", "userPwd": "6de72f7fa38ec95a5242986c000928394ba93fba",
        "userPwdMd5": "1c0f70cb097bd6ed821419a3a2b29da0", "username": "18888888810", "channelCode": "95155",
        "appVersion": "2.0.2", "mobileModel": "MX4 Pro", "protocolVersion": "1.0", "sourceSystem": "5.0.1",
        "sign": "c7f457fc948076d7ba15163fb55746ae"}
data = urllib.urlencode({'p': login_data})
h = httplib.HTTPSConnection('test-appapis.gghypt.net')
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
h.request('POST', '/AppService/userAction!login.action', data, headers)
r = h.getresponse()
print r.read()
