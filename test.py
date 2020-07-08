from bs4 import BeautifulSoup
from pprint import pprint


def has_class_id(tag):
    
    return tag.has_attr("class") and "c" in tag.get("class") and tag.has_attr("id") and tag.get("id").find("C_") == 0


with open("comment.html", "r", encoding="utf-8") as fr:
    soup = BeautifulSoup(fr.read(), "lxml")
    comments = soup.find_all(has_class_id)
    print(len(comments))
    for item in comments:
        d = {}
        line = item.get_text()

        nick = line.find(":")
        d["reviewer"] = line[:nick].strip()

        jb = line.find("举报")
        d["content"] = line[nick+1:jb].strip()


        later = line[jb:]
        hf = later.find("回复")
        lz = later.find("来自")
        d["datetime"] = later[hf+2:lz].strip()

        pprint(d)
        print("======================================")
    # comments = [ item for item in soup.find_all(has_class_id) if "举报" in item.get_text() and "赞" in item.get_text() and "回复" in item.text() ]
    # print(len(comments))