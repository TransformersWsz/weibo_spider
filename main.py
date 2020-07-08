import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import re
import time

url = "https://s.weibo.com/weibo/%25E5%259C%25A8%25E7%25BA%25BF%25E6%2595%2599%25E8%2582%25B2"

s_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.68 Safari/537.36 Edg/84.0.522.28",
    "Cookie": "SINAGLOBAL=6761572192214.149.1590379231528; UOR=,,login.sina.com.cn; wvr=6; ALF=1625748675; SSOLoginState=1594212676; SCF=AvAg04NFIWjzdUrCsc_W24v02abdujuIleCVkwsiPATS5bGWFq0BFZlelfpbtF8kMubdQ3FCrDgqbLqYtGhxYMw.; SUB=_2A25yAbEXDeRhGeNH6FYS9CzPyDSIHXVRdqXfrDV8PUNbmtANLVHXkW9NStPFk5Lhf6Kr-1cD5BlK9hVz3syNMKeQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZoBfZykY5Ib0UaOb6xx.65JpX5KzhUgL.Fo-4e0B0Shz0e0n2dJLoIEQLxK-LBKBLBK.LxK-LBo2LBo2LxK-L1h.L1K2LxK-LB--LBKzp1K.pehMt; SUHB=0Yhh94k6Ao1bU-; _s_tentry=login.sina.com.cn; Apache=9588005215838.537.1594212685021; ULV=1594212685128:7:4:3:9588005215838.537.1594212685021:1594090581447; webim_unReadCount=%7B%22time%22%3A1594212691980%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A2%2C%22msgbox%22%3A0%7D"
}

s_params = {
    "q": "在线教育",
    "xsort": "hot",
    "timescope": "custom:2020-02-01-0:2020-05-01-0",
    "Refer": "g",
    "page": 1
}

c_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "cookie": "_T_WM=46026963971; ALF=1596770918; SCF=AvAg04NFIWjzdUrCsc_W24v02abdujuIleCVkwsiPATS4iJro4emHJ9eXtV2weCW-IIEkIJFjHno3EW4nPnscL4.; SUB=_2A25yAU3eDeRhGeNH6FYS9CzPyDSIHXVRClOWrDV6PUJbktANLRPkkW1NStPFk3i6Lo1d6mJ0XsbeiHUxgDTAETUw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZoBfZykY5Ib0UaOb6xx.65JpX5K-hUgL.Fo-4e0B0Shz0e0n2dJLoIEQLxK-LBKBLBK.LxK-LBo2LBo2LxK-L1h.L1K2LxK-LB--LBKzp1K.pehMt; SUHB=0LcixAYH3dLGsR; SSOLoginState=1594178958",
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


for i in range(36):    # 共36页
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


        # Second Part: 爬取该条微博的所有评论
        # d["comments"] = []
        # for c_i in range(50):
        #     comment_url = "https://weibo.cn/comment/{}?page={}".format(d["comment_identification"], c_i+1)
        #     c_r = requests.get(comment_url, headers=c_headers)
        #     print("current_url:> ", comment_url)
            
        #     c_soup = BeautifulSoup(c_r.text, "lxml")

        #     def has_class_id(tag):
        #         return tag.has_attr("class") and "c" in tag.get("class") and tag.has_attr("id") and tag.get("id").find("C_") == 0

        #     comments = c_soup.find_all(has_class_id)
        #     if len(comments) == 0:
        #         break
        #     else:
        #         for item in comments:
        #             temp = {}
        #             temp["current_comment_page"] = c_i+1

        #             line = item.get_text()
        #             nick_suffix = line.find(":")
        #             temp["reviewer"] = line[:nick_suffix].strip()

        #             jb_suffix = line.find("举报")
        #             temp["content"] = line[nick_suffix+1:jb_suffix].strip()

        #             later = line[jb_suffix:]
        #             hf = later.find("回复")
        #             lz = later.find("来自")
        #             temp["datetime"] = later[hf+2:lz].strip()

        #             d["comments"].append(temp)
        #             pprint(temp)

        #             print("=====================================")
        #     time.sleep(10)
        #     print("当前第{}评论页爬取结束！\n".format(c_i+1))
        time.sleep(10)
    
        with open("./link/{}.json".format(d["comment_identification"]), "w", encoding="utf-8") as fw:
            json.dump(d, fw, ensure_ascii=False, indent=4)
        pprint(d)
        print("============================================================")
            
    print("当前第{}微博面爬取结束！\n".format(i+1))



