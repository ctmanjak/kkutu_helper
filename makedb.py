import json
import copy
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup

f = open("kkutu.json", "r", encoding='utf-8')
list = json.load(f)
if len(list) < 1: list.append({})
if not "일반" in list[0]: list[0]["일반"] = {}
if not "한방" in list[0]: list[0]["한방"] = {}
# 공격 방어 단어
url = "https://namu.wiki/w/%EB%81%84%ED%88%AC%EC%BD%94%EB%A6%AC%EC%95%84/%EA%B3%B5%EA%B2%A9%20%EB%B0%8F%20%EB%B0%A9%EC%96%B4%20%EB%8B%A8%EC%96%B4"
tablenum = 2
# 긴 단어
# url = "https://namu.wiki/w/%EB%81%84%ED%88%AC%EC%BD%94%EB%A6%AC%EC%95%84/%EA%B8%B4%20%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4"
# tablenum = 4
connect = urllib.request.urlopen(url)
content = connect.read().decode('utf-8')
soup = BeautifulSoup(content, 'html.parser')
for idx, table in enumerate(soup("table")):
    if idx >= tablenum:
        for p in table("p"):
            if p.next_element.name == "strong":
                p = p.next_element
            fullword = str(p.next_element.string)
            firstword = fullword[0]
            if fullword.isdigit() == False and fullword != "-" and fullword != "None" and fullword.find("[") == -1:
                if str(p).find("[한방]") == -1:
                    if not firstword in list[0]["일반"]:
                        list[0]["일반"][firstword] = []
                    if list[0]["일반"][firstword].count(fullword) == 0:
                        list[0]["일반"][firstword].append(fullword)
                else:
                    if not firstword in list[0]["한방"]:
                        list[0]["한방"][firstword] = []
                    if list[0]["한방"][firstword].count(fullword) == 0:
                        list[0]["한방"][firstword].append(fullword)
                        # if prevfirstword != firstword:
                        #     if prevfirstword in list:
                        #         list[0]["일반"][prevfirstword].extend(templist)
                        #     else:
                        #         list[0]["일반"][prevfirstword] = copy.deepcopy(templist)
                        #     templist.clear()
                        # templist.append(fullword)
                        # prevfirstword = firstword

# if prevfirstword in list:
#     list[prevfirstword].extend(templist)
# else:
#     list[prevfirstword] = copy.deepcopy(templist)


# for table in soup("table"):
#     for p in table:
#         print(p.next_element)
    # if len(str(string.string)) >= 9:
    #     list.append(str(string.string))
f.close()
f = open("kkutu.json", "w", encoding='utf-8')
json.dump(list, f, ensure_ascii=False)
f.close()
