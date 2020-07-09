import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import re
import time
import os
import random

from config import dirname, page_num, q, url

link_dir = "./{}/link".format(dirname)

s_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.68 Safari/537.36 Edg/84.0.522.28",
    "Cookie": "SINAGLOBAL=6761572192214.149.1590379231528; un=13776103604; wvr=6; ALF=1625824677; SSOLoginState=1594288737; SCF=AvAg04NFIWjzdUrCsc_W24v02abdujuIleCVkwsiPATScaJmm2OKihdvhkAkM0Wjm_ueeuBC254PQ-Dba6rZxFg.; SUB=_2A25yApo0DeRhGeNH6FYS9CzPyDSIHXVReYz8rDV8PUNbmtAKLXnmkW9NStPFkygyVuZvJwMe9iy0du8v5HGHu-1-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZoBfZykY5Ib0UaOb6xx.65JpX5KzhUgL.Fo-4e0B0Shz0e0n2dJLoIEQLxK-LBKBLBK.LxK-LBo2LBo2LxK-L1h.L1K2LxK-LB--LBKzp1K.pehMt; SUHB=0V5VHARiXKig3w; _s_tentry=login.sina.com.cn; Apache=7221364770733.112.1594288747506; ULV=1594288747868:8:5:4:7221364770733.112.1594288747506:1594212685128; UOR=,,www.google.com; WBStorage=42212210b087ca50|undefined; webim_unReadCount=%7B%22time%22%3A1594313040753%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A2%2C%22msgbox%22%3A0%7D"
}

s_params = {
    "q": q,
    "xsort": "hot",
    "timescope": "custom:2020-02-01-0:2020-05-01-0",
    "Refer": "g",
    "page": 1
}


def get_comment_identification(href):
    begin = 0
    end = 0
    f = re.finditer("/", href)
    for i in f:
        begin = i.span()[1]

    end = href.find("?")
    return href[begin:end]


for i in range(page_num):    # 共36页
    s_params["page"] = str(i+1)
    r = requests.get(url, params=s_params, headers=s_headers)

    soup = BeautifulSoup(r.text, "lxml")
    card_wraps = soup.find_all("div", attrs={"action-type": "feed_list_item"})
    
    for idx, each in enumerate(card_wraps):
        d = {}    # 每条微博的数据
        d["current_article_page"] = idx+1

        # First Part
        def has_node_type_nick_name(tag):
            return tag.has_attr("node-type") and tag.has_attr("nick-name")

        d["nick-name"] = each.find(has_node_type_nick_name)["nick-name"]    # 昵称

        d["content"] = re.sub("\u200b", "", each.find(has_node_type_nick_name).get_text().strip())    # 正文内容
        if "展开全文" in d["content"]:
            d["content"] = re.sub("\u200b", "", each.find("p", attrs={"node-type": "feed_list_content_full"}).get_text().strip())

        from_ = each.find("p", class_="from").find_all("a")
        d["datetime"] = from_[0].string.strip().replace("\n", " ")    # 日期时间
        d["comment_identification"] = get_comment_identification(from_[0]["href"])    # 评论链接
        if len(from_) == 2:
            d["source"] = from_[1].string.strip().replace("\n", "").replace(" ", "")    # 发布来源

        card_act = each.find("div", class_="card-act")
        d["forward_num"] = card_act.find("a", attrs={"action-type": "feed_list_forward"}).string.strip().split()[-1]    # 转发数
        d["comment_num"] = card_act.find("a", attrs={"action-type": "feed_list_comment"}).string.strip().split()[-1]    # 评论数
        d["like_num"] = card_act.find("a", attrs={"action-type": "feed_list_like"}).get_text().strip()    # 点赞数

        
    
        with open(os.path.join(link_dir, "{}.json".format(d["comment_identification"])), "w", encoding="utf-8") as fw:
            json.dump(d, fw, ensure_ascii=False, indent=4)
        pprint(d)
        print("============================================================")
    
    print("当前第{}微博面爬取结束！\n".format(i+1))
    time.sleep(random.uniform(5, 10))



