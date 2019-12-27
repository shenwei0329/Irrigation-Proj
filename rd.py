# -*- coding: utf-8 -*-
#

import sys, os, time
import urllib 
from bs4 import BeautifulSoup

from pyltp import SentenceSplitter, Segmentor, Postagger

seg = Segmentor()
seg.load("ltp_data_v3.4.0/cws.model")
pos = Postagger()
pos.load("ltp_data_v3.4.0/pos.model")

url_list = []

# Objects
#
names = []

_list = names

for _l in _list:
    if os.path.isfile(_l+".txt"):
        continue
    if _l not in url_list:
        url_list.append((_l,0))

if len(sys.argv)>1:
    if sys.argv[1] not in url_list:
        url_list.append((sys.argv[1],0))

_cnt = 0
_lvl = 0
for _url in url_list:
    if os.path.isfile("./TXT/"+_url[0]+".txt"):
        continue
    print("%s-%s" % (_url[0], _url[1]))
    _lvl = _url[1]
    url = "https://baike.baidu.com/item/" + _url[0]
    # print url[0]
    try:
        r = urllib.urlopen(url)
    except:
    # except Exception, e:
        # print e, e.message
        time.sleep(30)
        continue
    html = r.read()
    f = open("./TXT/"+_url[0]+".html", "w")
    f.write(html)
    f.close()

    soup = BeautifulSoup(html, "lxml")
    re = soup.select(".para")
    f = open("./TXT/"+_url[0]+".txt", "wb")
    for _i in range(len(re)):
        _str = re[_i].get_text().encode("utf-8")
        # print _str
        f.write(_str)
        if len(url_list) > 100000:
            continue
        _ss = SentenceSplitter.split(_str)
        for _s in _ss:
            words = seg.segment(_s)
            poss = pos.postag(words)
            for _word, _pos in zip(words, poss):
                if len(_word) > 4 and "nh" in _pos:
                    _word = _word.replace("/", "-").replace("（", "")
                    if os.path.isfile("./TXT/"+_word + ".txt"):
                        continue
                    if _lvl < 2 and (_word, _lvl+1) not in url_list:
                        print(">>> Add: "),
                        print(_word), _lvl+1
                        url_list.append((_word,_lvl+1))
    f.close()
    _cnt += 1
    if _cnt > 20:
        print("... Waiting")
        time.sleep(10)
        _cnt = 0
