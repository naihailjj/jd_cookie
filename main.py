import os
import json
import qrcode
import time
import pyperclip
import requests
import threading
requests.packages.urllib3.disable_warnings()
os.environ['no_proxy'] = '*'

jd_ua = 'jdapp;android;10.0.5;11;0393465333165363-5333430323261366;network/wifi;model/M2102K1C;osVer/30;appBuild/88681;partner/lc001;eufv/1;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 11; M2102K1C Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045534 Mobile Safari/537.36'


def token_get():
    t = round(time.time())
    headers = {
        'User-Agent': jd_ua,
        'referer': 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state={0}&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
    }
    t = round(time.time())
    url = 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state={0}&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
    res = s.get(url=url, headers=headers, verify=False)
    res_json = json.loads(res.text)
    s_token = res_json['s_token']
    token_post(s_token)
    # return s_token


def token_post(s_token):
    t = round(time.time() * 1000)
    headers = {
        'User-Agent': jd_ua,
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?s_token={0}&v={1}&remember=true'.format(s_token, t)
    data = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state={0}returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
        }
    res = s.post(url=url, headers=headers, data=data, verify=False)
    # print(res.text)
    res_json = json.loads(res.text)
    token = res_json['token']
    # print("token:", token)
    c = s.cookies.get_dict()
    okl_token = c['okl_token']
    # print("okl_token:", okl_token)
    t1 = threading.Thread(target=image_print, args=(token,))
    t2 = threading.Thread(target=check_token, args=(token, okl_token))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def check_token(token, okl_token):
    t = round(time.time() * 1000)
    headers = {
        'User-Agent': jd_ua,
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?&token={0}&ou_state=0&okl_token={1}'.format(token, okl_token)
    data = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action'.format(t),
        'source': 'wq_passport',
    }
    res = s.post(url=url, headers=headers, data=data, verify=False)
    check = json.loads(res.text)
    code = check['errcode']
    message = check['message']
    while code == 0:
        print("扫码成功")
        jd_ck = s.cookies.get_dict()
        pt_key = 'pt_key=' + jd_ck['pt_key']
        pt_pin = 'pt_pin=' + jd_ck['pt_pin']
        ck = str(pt_key) + ';' + str(pt_pin) + ';'
        print(ck)
        pyperclip.copy(ck)
        print("已复制到剪切板")
        break
    else:
        print(message)
        time.sleep(1)
        check_token(token, okl_token)


def image_print(token):
    qrurl = 'https://plogin.m.jd.com/cgi-bin/m/tmauth?client_type=m&appid=300&token={0}'.format(token)
    print("如果系统未弹出二维码图片, 请手动生成二维码")
    print("URL地址已复制到剪切板, 请使用在线二维码生成")
    print(qrurl)
    pyperclip.copy(qrurl)
    try:
        img = qrcode.make(qrurl)
        img.show()
    except:
        print('二维码生成失败, 请手动在线生成')
        print(qrurl)


if __name__ == '__main__':
    os.system('chcp 65001')
    print("Ver: 1.0 By: limoe")
    print("https://github.com/Zy143L/jd_cookie")
    print("JD扫码获取Cookie")
    print("回车生成二维码")
    input()
    s = requests.session()
    token_get()
    os.system('pause')
