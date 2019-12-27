# coding: utf-8
#

import sys
import json
import p_loader

type_info = [
             '',
             '新闻',
             '论坛',
             '博客',
             '微博',
             'APP',
             '微信',
             '电子报',
            ]

for _item in p_loader.names:

    _fn = "./TXT/%s/" % sys.argv[1] + _item + '.html'
    # print(_fn)

    with open(_fn, "r") as f:
        _str = f.read()
        f.close()
        _rec = json.loads(_str)
        # {u'resultData': {u'SY_SECTIONTIDS': 7, u'dataList': [], u'databasic': {u'allcount': 0, u'allpages': 0, u'pagesize': 10, u'pageno': 1}}, u'resultCode': u'200', u'resultState': u'success'}
        if _rec['resultCode'] == u'200' and _rec['resultState'] == u'success':
            
            if _rec['resultData']['databasic']['allcount'] > 0:
                print("[{}]".format(_item))
                for _u in _rec['resultData']['dataList']:
                    # print(_u.keys())
                    print(u"\t> RID: {}".format(_u["RID"]))
                    print(u"\t> UrlTime: {}".format(_u["IR_URLTIME"]))
                    print(u"\t> UrlTitle: {}".format(_u["IR_URLTITLE"]))
                    print(u"\t> Url: {}".format(_u["IR_URLNAME"]))
                    print(u"\t> SiteName: {}".format(_u["IR_SITENAME"]))
                    print(u"\t> Authors: {}".format(_u["IR_AUTHORS"]))
                    print(u"\t> Channel: {}".format(_u["IR_CHANNEL"]))
                    print(u"\t> BBcommon: {}".format(_u["SY_BB_COMMON"]))
                    print("\t> InfoType: {}".format(type_info[_u["SY_INFOTYPE"]]))
                    print(u"\t> Abstrace: {}".format(_u["IR_ABSTRACT"]))
                    print(u"\t> Content:\n{}".format(_u["IR_CONTENT"].replace("\n", "^").replace("\r", "")))
                    print("\t----")

                print("*"*8)

# Eof

