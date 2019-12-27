# -*- coding:UTF-8 -*-
#

import sys
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from pyltp import SentenceSplitter
from pyltp import NamedEntityRecognizer
import re

seg = Segmentor()
seg.load_with_lexicon('ltp_data_v3.4.0/cws.model', './ext_word')
post = Postagger()
post.load_with_lexicon('ltp_data_v3.4.0/pos.model', './ext_word_pos')
recognizer = NamedEntityRecognizer()
recognizer.load('ltp_data_v3.4.0/ner.model')
parser = Parser()
parser.load('ltp_data_v3.4.0/parser.model')


def segmentor(sentence):
    """

    :param sentence:
    :return:
    """
    global seg
    words = seg.segment(sentence)
    words_list = list(words)
    return words_list


def postagger(words):
    """

    :param words:
    :return:
    """
    global post
    pos = post.postag(words)
    pos_list = list(pos)
    return pos_list


def getdate(word):
    """

    :param word:
    :return:
    """

    if ("春" in word) or ("夏" in word) or ("秋" in word) or ("冬" in word):
        return word

    if "月" in word:
        _sentence = word.replace('十一月', '11月').replace('十二月', '12月')
        _sentence = _sentence.replace('一月', '1月').replace('二月', '2月').replace('三月', '3月'). \
            replace('四月', '4月').replace('五月', '5月')
        _sentence = _sentence.replace('六月', '6月').replace('七月', '7月').replace('八月', '8月'). \
            replace('九月', '9月').replace('十月', '10月')
    else:
        _sentence = word

    m = re.search(r"(\d+)月", _sentence)
    if m is not None:
        _m = int(m.group(0).split("月")[0])
        if (_m < 13) and (_m > 0):
            return _m
    return None


def hasSBV(arcs):
    """

    :param arcs:
    :return:
    """
    sbv = False
    vob = False
    hed = False
    for nn in arcs:
        if "SBV" in nn.relation:
            sbv = True
        if "VOB" in nn.relation:
            vob = True
        if "HED" in nn.relation:
            hed = True
    if (hed and sbv) or (vob and sbv):
        return True
    return False


def chs_replace(sentence):
    """

    :param sentence:
    :return:
    """
    _s = sentence.replace("零", "0")
    _s = _s.replace("一", "1").replace("二", "2").replace("三", "3")
    _s = _s.replace("四", "4").replace("五", "5").replace("六", "6")
    _s = _s.replace("七", "7").replace("八", "8").replace("九", "9")

    _n_idx = 0
    while True:
        _idx = _s.find("十", _n_idx)
        if _idx < 0:
            break
        if _idx == _n_idx:
            break
        if _idx > 0:
            if _s[_idx-1:_idx].isdigit():
                if _s[_idx+3:_idx+4].isdigit():
                    _s = _s[:_idx] + _s[_idx+3:]
                else:
                    _s = _s[:_idx] + "0" + _s[_idx+3:]
            else:
                if _s[_idx+3:_idx+4].isdigit():
                    _s = _s[:_idx] + "1" + _s[_idx+3:]

        _n_idx = _idx
    return _s


year = None
month = None
events = {}
line_cnt = 0

"""获取文本文件"""
f = open(sys.argv[1])

while True:

    """读一段文本"""
    sentence = f.readline()
    if (sentence is "") or (len(sentence) == 0):
        """ Eof """
        break

    """替代中文引号"""
    sentence = sentence.replace("‘", "").replace("’", "").replace("”", "").replace("“", "")
    line_cnt += 1

    """断句"""
    sents = SentenceSplitter.split(sentence)

    for ss in sents:

        s = chs_replace(ss)
        """语句处理"""
        words = segmentor(s)
        pos = postagger(words)
        netags = list(recognizer.recognize(words, pos))
        arcs = list(parser.parse(words, pos))
        _i = 0
        for _p in pos:
            if "nt" in _p:
                if "年" in words[_i]:
                    _y = words[_i].split("年")[0]
                    if str(_y).isdigit():
                        _y = int(_y)
                        if (_y > 1000) and (_y < 2024):
                            year = _y
                else:
                    _m = getdate(words[_i])
                    if _m is not None:
                        month = _m
            """Next"""
            _i += 1

        if hasSBV(arcs) and (year is not None):
            if year not in events:
                events[year] = {}
            if month not in events[year]:
                events[year][month] = {}
                events[year][month]['sentence'] = 0
                events[year][month]['word'] = 0
            events[year][month]['sentence'] += 1
            events[year][month]['word'] += len(words)

for _date in sorted(events, key=lambda x: x):
    print("%s年：" % str(_date))
    for _m in sorted(events[_date], key=lambda x: x):
        if str(_m).isdigit():
            print("\t%s月\t%3d\t[" % (_m, events[_date][_m]['sentence'])),
        else:
            print("\t%s\t%3d\t[" % (_m, events[_date][_m]['sentence'])),

        print("+" * events[_date][_m]['sentence']),
        # print("-" * events[_date][_m]['word']),
        print(" ]")

parser.release()
post.release()
seg.release()

print("Done.")
