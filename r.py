import requests
from bs4 import BeautifulSoup
from pprint import pprint as print
import json
import re
import time

url = "https://s.weibo.com/weibo/%25E5%259C%25A8%25E7%25BA%25BF%25E6%2595%2599%25E8%2582%25B2"

s_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.68 Safari/537.36 Edg/84.0.522.28",
    "Cookie": "SINAGLOBAL=6761572192214.149.1590379231528; SSOLoginState=1594090574; _s_tentry=login.sina.com.cn; Apache=4564164926965.429.1594090581416; UOR=,,login.sina.com.cn; ULV=1594090581447:6:3:2:4564164926965.429.1594090581416:1594033185529; wvr=6; webim_unReadCount=%7B%22time%22%3A1594175407557%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A2%2C%22msgbox%22%3A0%7D; SCF=AvAg04NFIWjzdUrCsc_W24v02abdujuIleCVkwsiPATSDWeXoh5mp5J8xx442-tiAMsrK-_88M6zmKOMAtqJdZM.; SUB=_2A25yAU05DeRhGeNH6FYS9CzPyDSIHXVRdznxrDV8PUNbmtAKLUTbkW9NStPFkwrrIcJ7__NVsQcUiqrBthUZ7i8c; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZoBfZykY5Ib0UaOb6xx.65JpX5KMhUgL.Fo-4e0B0Shz0e0n2dJLoIEQLxK-LBKBLBK.LxK-LBo2LBo2LxK-L1h.L1K2LxK-LB--LBKzp1K.pehMt; SUHB=0z1wUf2dzPCjxh; ALF=1625714825"
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
    "cookie": "_T_WM=46026963971; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4499539304421029%26luicode%3D20000061%26lfid%3D4499539304421029; ALF=1596770918; SCF=AvAg04NFIWjzdUrCsc_W24v02abdujuIleCVkwsiPATS4iJro4emHJ9eXtV2weCW-IIEkIJFjHno3EW4nPnscL4.; SUB=_2A25yAU3eDeRhGeNH6FYS9CzPyDSIHXVRClOWrDV6PUJbktANLRPkkW1NStPFk3i6Lo1d6mJ0XsbeiHUxgDTAETUw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZoBfZykY5Ib0UaOb6xx.65JpX5K-hUgL.Fo-4e0B0Shz0e0n2dJLoIEQLxK-LBKBLBK.LxK-LBo2LBo2LxK-L1h.L1K2LxK-LB--LBKzp1K.pehMt; SUHB=0LcixAYH3dLGsR; SSOLoginState=1594178958",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.68 Safari/537.36 Edg/84.0.522.28"
}


r = requests.get(url, params=s_params, headers=s_headers)
with open("weibo.html", "w", encoding="utf-8") as fw:
    fw.write(r.text)
print(r.text)



