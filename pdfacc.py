# -*- coding: utf-8 -*-
import json
import requests

REQUEST_URL = "http://10.111.30.195:8181/api/v1.0/ltps"
HEADER = {'Content-Type':'application/json; charset=utf-8'}

def ltp_service(text):
    # requestDict = {'text':text, 'cmd':['pos', 'recog']}
    requestDict = {'text':text, 'cmd':['pos', 'recog', 'pars']}
    rsp = requests.post(REQUEST_URL, data=json.dumps(requestDict), headers=HEADER)
    if rsp.status_code == 201:
        rt =  json.loads(rsp.text)
        for _s in rt['ltp']:
            # print _s
            _idx = 0
            for _k in _s['pos']:
                print _k, _s['words'][_idx],
                _idx += 1
            print ""
            _idx = 0
            for _k in _s['recog']:
                if "-N" in _k:
                    print _k, _s['words'][_idx]
                _idx += 1
            print ""
            """
            _link = {}
            for _k in _s['pars']:
                if _k[0] not in _link:
                    _link[_k[0]] = {"id": _k[1], "type": _k[2], "link": []}
                else:
                    _link[_k[0]]["link"].append({"id": _k[1], "type": _k[2]})
            print _link
            """
        return True
    else:
        return False
    
# 程序入口函数
if __name__=="__main__":

    ltp_service(u"大连万达俱乐部在决赛后，因对裁判员判罚不满，而拒绝领奖和不出席新闻发布会。这种行为不仅不符合体育精神，不符合足球比赛的规范，也有损于大连万达俱乐部和中国足球的形象。对此，中国足球协会特通报批评。大连万达俱乐部应认真检查，吸取教训，并准备接受亚足联可能给予的处罚。")

    ltp_service(u"巴希尔强调，政府坚决主张通过和平和政治途径结束目前的武装冲突，在全国实现和平。他强烈呼吁以约翰·加朗为首的反政府武装力量回到国家的怀抱。在谈到周边关系时，巴希尔说，苏丹政府将采取行动改善与周边国家的关系。")

    ltp_service(u"2019年4月19日，一九八四年四月和一九八五年一季度，利用电科华云dummyDriver将vmware存量虚拟机纳管到电科华云基础设施管理云平台，进而实现电科华云基础设施管理云平台对存量虚拟机的使用及管理，并且支持从电科华云基础设施管理云平台释放（该虚拟机在电科华云基础设施管理云平台上删除但仍存在于vcenter中）已纳管的存量虚拟机。")
