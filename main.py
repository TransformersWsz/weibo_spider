import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

url = "https://s.weibo.com/weibo/%25E5%259C%25A8%25E7%25BA%25BF%25E6%2595%2599%25E8%2582%25B2"

s_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.68 Safari/537.36 Edg/84.0.522.28",
    "Cookie": "SINAGLOBAL=6761572192214.149.1590379231528; un=13776103604; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZoBfZykY5Ib0UaOb6xx.65JpX5KMhUgL.Fo-4e0B0Shz0e0n2dJLoIEQLxK-LBKBLBK.LxK-LBo2LBo2LxK-L1h.L1K2LxK-LB--LBKzp1K.pehMt; ALF=1625626570; SSOLoginState=1594090574; SCF=AvAg04NFIWjzdUrCsc_W24v02abdujuIleCVkwsiPATSl5nLJSDRs6bBuhmeQT2jr114hUOqv07hjQaS90VYMF0.; SUB=_2A25yB5QfDeRhGeNH6FYS9CzPyDSIHXVRdILXrDV8PUNbmtAKLVn5kW9NStPFk3MUB6O24pkPw493t1qYriDS-2oX; SUHB=0qjEYBE0W-TD6a; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=4564164926965.429.1594090581416; ULV=1594090581447:6:3:2:4564164926965.429.1594090581416:1594033185529; wvr=6; webim_unReadCount=%7B%22time%22%3A1594105683849%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A14%2C%22msgbox%22%3A0%7D; WBStorage=42212210b087ca50|undefined"
}

s_params = {
    "q": "在线教育",
    "xsort": "hot",
    "timescope": "custom:2020-02-01-0:2020-05-01-0",
    "Refer": "g",
    "page": 1
}

data = []

# for i in range(36):
#     s_params["page"] = str(i+1)
#     r = requests.get(url, params=s_params, headers=s_headers)

#     with open("weibo.html", "w", encoding="utf-8") as fw:
#         fw.write(r.text)
#     break

#     # d = {}
#     # soup = BeautifulSoup(r.text, "html.parser")
#     # cards = soup.find_all("div", class_="card")

#     # for each in cards:

#     #     def has_node_type_nick_name(tag):
#     #         return tag.has_attr("node-type") and tag.has_attr("nick-name")


#     #     nick_name = each.find(has_node_type_nick_name)
#     #     print(nick_name["nick-name"])
#     # break


with open("weibo.html", "r", encoding="utf-8") as fr:
    txt = fr.read()
    soup = BeautifulSoup(txt, "html.parser")
    card_wraps = soup.find_all("div", attrs={"action-type": "feed_list_item"})

    d = {}
    for each in card_wraps:
        
        def has_node_type_nick_name(tag):
            return tag.has_attr("node-type") and tag.has_attr("nick-name")

        d["nick-name"] = each.find(has_node_type_nick_name)["nick-name"]    # 昵称

        d["content"] = re.sub("\u200b", "", each.find(has_node_type_nick_name).get_text().strip())    # 正文内容
        if "展开全文" in d["content"]:
            d["content"] = re.sub("\u200b", "", each.find("p", attrs={"node-type": "feed_list_content_full"}).get_text().strip())

        from_ = each.find("p", class_="from").find_all("a")
        d["datetime"] = from_[0].string.strip().replace("\n", " ")    # 日期时间
        if len(from_) == 2:
            d["source"] = from_[1].string.strip().replace("\n", "").replace(" ", "")    # 发布来源

        card_act = each.find("div", class_="card-act")
        d["forward"] = card_act.find("a", attrs={"action-type": "feed_list_forward"}).string.strip().split()[-1]    # 转发数
        d["comment"] = card_act.find("a", attrs={"action-type": "feed_list_comment"}).string.strip().split()[-1]    # 评论数
        d["like"] = card_act.find("a", attrs={"action-type": "feed_list_like"}).get_text().strip()    # 点赞数

        pprint(d)

        print("======================done===============")