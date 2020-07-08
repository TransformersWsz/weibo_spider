import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import re
import time
import glob



c_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "cookie": "_T_WM=46026963971; ALF=1596804676; SCF=AvAg04NFIWjzdUrCsc_W24v02abdujuIleCVkwsiPATSlPtON0FTL0ud5t4S69fu9K6EaQgrYwnRVh_g2IeMSq0.; SUB=_2A25yAY3tDeRhGeNH6FYS9CzPyDSIHXVRDROlrDV6PUJbktAKLWT4kW1NStPFkz2taCZ2p6DXY5W625diwGmlzBho; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZoBfZykY5Ib0UaOb6xx.65JpX5K-hUgL.Fo-4e0B0Shz0e0n2dJLoIEQLxK-LBKBLBK.LxK-LBo2LBo2LxK-L1h.L1K2LxK-LB--LBKzp1K.pehMt; SUHB=0idbWDPGNxPKIp; SSOLoginState=1594228157",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.68 Safari/537.36 Edg/84.0.522.28"
}


def get_comment_identification(href):
    begin = 0
    end = 0
    f = re.finditer("/", href)
    for i in f:
        begin = i.span()[1]

    end = href.find("?")
    return href[begin:end]


idfiles = glob.glob("./link/*.json")
for json_file in idfiles:
    
    with open(json_file, "r", encoding="utf-8") as fr:
        json_data = json.load(fr)

        # Second Part: 爬取该条微博的所有评论
        d = []
        for c_i in range(50):
            comment_url = "https://weibo.cn/comment/{}?page={}".format(json_data["comment_identification"], c_i+1)
            c_r = requests.get(comment_url, headers=c_headers)
            print("current_url:> ", comment_url)
            
            c_soup = BeautifulSoup(c_r.text, "lxml")

            def has_class_id(tag):
                return tag.has_attr("class") and "c" in tag.get("class") and tag.has_attr("id") and tag.get("id").find("C_") == 0

            comments = c_soup.find_all(has_class_id)
            if len(comments) == 0:
                break
            else:
                for item in comments:
                    temp = {}
                    temp["current_url"] = comment_url
                    temp["current_comment_page"] = c_i+1

                    line = item.get_text()
                    nick_suffix = line.find(":")
                    temp["reviewer"] = line[:nick_suffix].strip()

                    jb_suffix = line.find("举报")
                    temp["content"] = line[nick_suffix+1:jb_suffix].strip()

                    later = line[jb_suffix:]
                    hf = later.find("回复")
                    lz = later.find("来自")
                    temp["datetime"] = later[hf+2:lz].strip()

                    d.append(temp)

                    pprint(temp)
                    print("=====================================")
            time.sleep(10)
            print("当前第{}评论页爬取结束！\n".format(c_i+1))

        with open("./comment/{}".format(json_data["comment_identification"]), "w", encoding="utf-8") as fw:
            json.dump(d, fw, ensure_ascii=False, indent=4)
        print("<------------------{}全部评论爬取结束---------------------->".format(json_data["comment_identification"]))
print("\n done! \n")

