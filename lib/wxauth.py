#coding:utf8
import requests
import redis_utils
import uuid
import json
from WXBizDataCrypt import WXBizDataCrypt

WXAPP_ID = 'wx28c8a74bd01f5e3a'
#WXAPP_ID = 'wx8e8fc77f7f2ef904'

WXAPP_SECRET = '1c7efd0054d7ac6aaa84b4205e6e3794'
#WXAPP_SECRET = '0624061fa7638f0538299c6973ff059a'



def get_wxapp_session_key(code, login_key):
    if login_key:
        key = login_key
    else:
        key = str(uuid.uuid1())
    redis_data = redis_utils.get_cache(key, refresh_expires=False)
    if redis_data:
        return json.loads(redis_data)
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code'%(WXAPP_ID, WXAPP_SECRET, code)

    data = requests.get(url).json()
    
    print data
    redis_utils.set_cache(key, json.dumps(data), 7200)
    return data, key


def get_user_info(encryptedData, iv, session_key):
    pc = WXBizDataCrypt(WXAPP_ID, session_key)
    return pc.decrypt(encryptedData, iv)

def get_wxcode():
    key = 'access_token'
    redis_data = redis_utils.get_cache(key, refresh_expires=False)
    if redis_data:
        token_data = json.loads(redis_data)
    else:
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(WXAPP_ID, WXAPP_SECRET)
        token_data = requests.get(url).json()
        redis_utils.set_cache(key, json.dumps(token_data), 7000)
    data = {
        #'path':'https://devkdysapi2.xiaoxianetwork.com/book/get_content?book_id=5373849&volume_id=2251&chapter_id=2199&platform=applet',
        'path': u'pages/reader/reader?book_id=185061&index=0',
        'width': 430,
        'auto_color': False
        #'line_color': {"r":"0","g":"0","b":"0"}
    }
    url_a = 'https://api.weixin.qq.com/wxa/getwxacode?access_token=%s'%token_data['access_token']
    headers = {'content-type': 'application/json'}
    a = requests.post(url_a, data=json.dumps(data), headers=headers)
    open('logo.jpg', 'wb').write(a.content)
    print 111
    return 111
