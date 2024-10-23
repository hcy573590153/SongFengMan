import os
import sys
from requests import get, post
import random
import datetime
import json
import time
from pathlib import Path
from loguru import logger



class YuanShanHeng:
    def __init__(self, config_path):
        with open(Path(config_path), "r", encoding="utf-8") as f:
            self.config = json.load(f)
            logger.add(Path("./log/ysh.log"))

    def pusher_dataloader(self, data_name, data):
        ret = {
            "touser": None,
            "template_id": self.config["templates"][data_name]["tpl_id"],
            "data": self.config["templates"][data_name]["message_data_tpl"]
        }
        for k in data.keys():
            ret["data"][k]["value"] = data[k]
        return ret

    def pusher(self, data):
        for u in self.config["users"]:
            data["touser"] = u
            response = post(self.config["send_url"] + access_token, json=data).json()
            logger.info("send:::" + str(data))
            logger.info("recv:::" + str(response))
            if response["errcode"] == 40037:
                logger.error("templ_id fail")
            elif response["errcode"] == 40036:
                logger.error("NO templ_id")
            elif response["errcode"] == 40003:
                logger.error("user id fail")
            elif response["errcode"] == 0:
                logger.success("push successfully")
            else:
                logger.error("unknown fail")


    def send_ranking_head(self, access_token, head):
        logger.info("push ranking_head")
        data = self.pusher_dataloader("ranking_head", head)
        self.pusher(data)
        
        

    def send_ranking_body(self, access_token, body):
        logger.info("push ranking_body")
        data = self.pusher_dataloader("ranking_body", body)
        self.pusher(data)
        

    def send_ranking(self, access_token, ranking):
        logger.info("push ranking start")
        self.send_ranking_head(access_token, ranking["head"])
        for b in ranking["bodys"]:
            self.send_ranking_body(access_token, b)
        logger.info("push ranking end")

    def send_instant_message(self, access_token, im):
        logger.info("push instant_message")
        data = self.pusher_dataloader("instant_message", im)
        self.pusher(data)
        

    def get_access_token(self):
        if Path("acc_temp.tmp").exists():
            with open(Path("acc_temp.tmp"), "r") as f:
                acc_temp = json.load(f)
            if time.time() < acc_temp["val"]:
                logger.info("use acc_temp access_token")
                return acc_temp["access_token"], None
        # appId
        app_id = self.config["app_id"]
        # appSecret
        app_secret = self.config["app_secret"]
        post_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
        try:
            get_res = get(post_url).json()
            access_token = get_res['access_token']
            expires_in = get_res['expires_in']
        except KeyError:
            logger.error("get access_token fail, please recheck app_id and app_secret")
            os.system("pause")
            sys.exit(1)
        acc_temp = {"access_token": access_token, "val": time.time() + 60*60}
        with open(Path("acc_temp.tmp"), "w") as f:
            json.dump(acc_temp, f, indent = 4)
        logger.info("refresh acc_temp access_token:" + str(get_res))
        return access_token, expires_in
    



if __name__ == '__main__':
    ysh = YuanShanHeng("yuanshanheng.ini")
    access_token, expires_in = ysh.get_access_token()

    ranking = {
        "head": {"ranking_name": "涨幅榜"},
        "bodys": [
            {
                "ranking_name": "涨幅榜",
                "intra_ranking": "1",
                "stock_id": "000000",
                "stock_name": "威威帆帆",
                "pred": "[2, 3] [2, 5]"
            }, 
            {
                "ranking_name": "涨幅榜",
                "intra_ranking": "2",
                "stock_id": "111111",
                "stock_name": "撒旦士大",
                "pred": "[2, 3] [2, 5]"
            }, 
            {
                "ranking_name": "涨幅榜",
                "intra_ranking": "3",
                "stock_id": "222222",
                "stock_name": "算法入门",
                "pred": "[2, 3] [2, 5]"
            }
        ]
    }
    ysh.send_ranking(access_token, ranking)

    im = {
            "type": "急涨预警",
            "importance": "1",
            "stock_id": "000000",
            "stock_name": "上证指数",
            "text": "5分钟内急速拉升，请关注",
            "tip": "考虑见顶卖出"
        }
    ysh.send_instant_message(access_token, im)

    im = {
            "type": "急涨预警",
            "importance": "1",
            "stock_id": "000000",
            "stock_name": "上证指数",
            "text": "5分钟内急速拉升，请关注",
            "tip": "考虑见顶卖出"
        }
    ysh.send_instant_message(access_token, im)

    im = {
            "type": "急涨预警",
            "importance": "1",
            "stock_id": "000000",
            "stock_name": "上证指数",
            "text": "5分钟内急速拉升，请关注",
            "tip": "考虑见顶卖出"
        }
    ysh.send_instant_message(access_token, im)

    im = {
            "type": "急涨预警",
            "importance": "1",
            "stock_id": "000000",
            "stock_name": "上证指数",
            "text": "5分钟内急速拉升，请关注",
            "tip": "考虑见顶卖出"
        }
    ysh.send_instant_message(access_token, im)


