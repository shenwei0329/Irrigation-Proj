# -*- coding: utf-8 -*-
import json
import requests

REQUEST_URL = "http://10.111.30.195:8181/api/v1.0/ltps"
HEADER = {'Content-Type':'application/json; charset=utf-8'}

def ltp_service(text, cmd):
    # cmd = ['seg'] or ['pos','recog','pars']
    requestDict = {'text':text, 'cmd':cmd}
    rsp = requests.post(REQUEST_URL, data=json.dumps(requestDict), headers=HEADER)
    if rsp.status_code == 201:
        rt =  json.loads(rsp.text)
        return rt['ltp']
 
# 程序入口函数
if __name__=="__main__":

    rt = ltp_service(u"签约仪式前，秦光荣、李纪恒、仇和等一同会见了参加签约的企业家。", ['pos','recog'])
    for _w in zip(rt[0]['words'],rt[0]['pos']):
        print(u"{}:{}".format(_w[0],_w[1])),

    print("")
#

