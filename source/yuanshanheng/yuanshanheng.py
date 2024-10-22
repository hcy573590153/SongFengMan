import os
import sys
from requests import get, post
import random
import datetime
import json
import time



# 获取token
def get_access_token(config):
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    try:
        get_res = get(post_url).json()
        print(get_res)
        access_token = get_res['access_token']
        expires_in = get_res['expires_in']
    except KeyError:
        print("get access_token fail, please recheck app_id and app_secret")
        os.system("pause")
        sys.exit(1)
    return access_token, expires_in


"""
榜单归属                {{n1.DATA}}
榜内排行                {{n2.DATA}}
股票代码                {{n3.DATA}}
股票名称                {{n4.DATA}}
持仓                       {{n5.DATA}}
"""



# 推送
def send_message(config, access_token, p):
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"

    # 准备发送数据
    data = {
        "touser": None,
        "template_id": config["template_id"],
        # 点击事件目标url
        "data": {
            "n1": {
                "value":None
            },
            "n2": {
                "value":None
            },
            "n3": {
                "value":None
            },
            "n4": {
                "value":None
            },
            "n5": {
                "value":None
            }
        }
    }

    for u in config["users"]:
        data["touser"] = u
        response = post(
            send_url, 
            # headers=config["headers"], 
            json=data).json()
        print(response)
        if response["errcode"] == 40037:
            print("templ_id fail")
        elif response["errcode"] == 40036:
            print("NO templ_id")
        elif response["errcode"] == 40003:
            print("推送消息失败，请检查微信号是否正确")
        elif response["errcode"] == 0:
            print("推送消息成功")
        else:
            print(response)

def send_ranking(access_token, ranking):
    send_ranking_head(access_token, ranking["head"])
    send_ranking_body(access_token, ranking["body"])




if __name__ == '__main__':
    # 加载配置文件
    try:
        with open("yuanshanheng.ini", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("no config")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("user id fail")
        os.system("pause")
        sys.exit(1)

    access_token, expires_in = get_access_token(config)
    print(access_token, expires_in)

    # # 推送消息
    for i in range(10):
        send_message(config, access_token, i+1)
        time.sleep(1)