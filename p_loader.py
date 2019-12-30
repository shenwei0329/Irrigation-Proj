# coding: utf-8
#

import sys, os, time
import urllib
import json
import mongodb_class
import put2db

#
# API
url = "http://210.12.196.17:8080/om/cus?id=48c8aa49&key=6afcca56&sid=64&pageNo=1&pageSize=10&kw="

# Objects
#
names = [
         # L1 River
         "潮白新河",
         "北运河",
         "东洋河",
         "妫水河",
         "二道河",
         "鄂卜平河",
         "浑河",
         "壶流河",
         "蓟运河",
         "金钟河",
         "南洋河",
         "桑干河",
         "洋河",
         "永定河",
         "永定新河",
         "北京排污河",

         # 水库
         "友谊水库",
         "官厅水库",
         "册田水库",

         # L2 River
         "白登河",
         "北沟",
         "大龙河",
         "凤港减河",
         "凤河",
         "古城河",
         "故卫干渠",
         "黑河",
         "黑水河",
         "黑猪河",
         "洪塘河",
         "黄水河",
         "恢河",
         "津唐运河",
         "口泉河",
         "梨益沟",
         "凉水河",
         "龙河",
         "马关河",
         "马峪河",
         "木瓜河",
         "清水河""",
         "瑟尔基后河",
         "十里河",
         "天堂河",
         "西龙湾沟",
         "西洋河",
         "小龙河",
         "新凤河",
         "新华营河",
         "阳河",
         "饮马河",
         "淤泥河",
         "御河",
         "源子河",

         # L1 SubRiver
         "东洋河",
         "妫水河",
         "浑河",
         "壶流河",
         "南洋河",
         "清水河",
         "御河",
         "西洋河",
         "黄水河",
         "源子河",
         "七里河",
         "恢河",

         # L3
         "巴音图河",
         "白家务碱河",
         "大沟河",
         "大淖海子",
         "大庄科河",
         "定安河",
         "东南郊灌渠",
         "妫水河",
         "黑河",
         "黄水河",
         "机场排水河",
         "郎园引河",
         "凉水河",
         "凌云口峪",
         "龙北新河",
         "马关河",
         "蔓菁沟",
         "牤牛河",
         "门头沟",
         "泥河",
         "七里河",
         "前河",
         "圈子河",
         "桑干河",
         "十七号河",
         "通惠灌渠",
         "王千庄峪",
         "吾其河",
         "西沟河",
         "谢家堡沟",
         "杨虎子河",
         "银子河",
         "永定河",
         "永定河引水渠",
         "永金引河",
         "鸳鸯河",
         "源子河",
         "镇川河",
         "正沟河",
         "中泓故道",
         "朱家营河",

        ]

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


def main():

    db = mongodb_class.mongoDB()
    db.connect_db("rivers")

    for _item in names:

        _url = url + _item

        try:
            r = urllib.urlopen(_url)
        except Exception as e:
            print(">>>Err: {}".format(e))
            continue

        html = r.read()

        _rec = json.loads(html)
        if _rec['resultCode'] == u'200' and _rec['resultState'] == u'success':

            if _rec['resultData']['databasic']['allcount'] > 0:
                print("[{}]".format(_item))
                for _u in _rec['resultData']['dataList']:

                    _sql = {"RID": _u["RID"]}
                    _cnt = db.handler("river", "find", _sql).count()
                    if _cnt == 0:

                        _u['Node'] = _item
                        db.handler("river", "update", _u, _u)

                        print("\t> RID: {}".format(_u["RID"]))
                        print("\t> UrlTime: {}".format(_u["IR_URLTIME"]))
                        print("\t> Url: {}".format(_u["IR_URLNAME"]))
                        print("\t----")

                print("*" * 8)

        time.sleep(5)

    # 更新图数据库
    put2db.main()


if __name__ == "__main__":
    main()


# Eof

