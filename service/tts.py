#!/usr/bin/python
# coding=utf-8
import sys
import json
import chardet
import os.path

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
# 这里使用了百度语音服务，请自行注册百度开发者获取相关权限
API_KEY = 'xxxxxxxxxxxxx'
SECRET_KEY = 'xxxxxxxxxxxxx'

TEXT = "807路";

# 发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
PER = 0
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 3

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
FORMAT = FORMATS[AUE]

CUID = "123456PYTHON"

TTS_URL = 'http://tsn.baidu.com/text2audio'


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """

def create_voice(bus, minutes):
    voice_file = 'audio/' + bus + '-' + minutes + '.' + FORMAT
    TEXT = bus + '公交车还有' + minutes + '分钟到站'
    if (bus == 'welcome'):
        TEXT = '欢迎使用语音公交'
        voice_file = 'audio/welcome-0.' + FORMAT
    if (bus == 'mute'):
        TEXT = '-'
        voice_file = 'audio/mute-0.' + FORMAT
    if (minutes == 'waiting'):
        TEXT = bus + '公交车正在等待发车'
        voice_file = 'audio/' + bus + '-waiting.' + FORMAT
    if (minutes == 'soon'):
        TEXT = bus + '公交车即将到站'
        voice_file = 'audio/' + bus + '-soon.' + FORMAT
    if os.path.isfile(voice_file):
        return
    print TEXT
    token = fetch_token()
    tex = quote_plus(TEXT.encode('utf-8'))
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)
    print('test on Web Browser' + TTS_URL + '?' + data)

    req = Request(TTS_URL, data.encode('utf-8'))

    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        has_error = ('content-type' not in f.headers.keys() or f.headers['content-type'].find('audio/') < 0)
    except  URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
        has_error = True

    save_file = "error.txt" if has_error else voice_file
    with open(save_file, 'wb') as of:
        of.write(result_str)

    if has_error:
        print("tts api  error:" + result_str)

    print("result saved as :" + save_file)