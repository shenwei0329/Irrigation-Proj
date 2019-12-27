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
seg.load_with_lexicon('ltp_data_v3.4.0/cws.model', './ext_word_cloud')
post = Postagger()
post.load_with_lexicon('ltp_data_v3.4.0/pos.model', './ext_word_cloud_pos')
recognizer = NamedEntityRecognizer()
recognizer.load('ltp_data_v3.4.0/ner.model')
parser = Parser()
parser.load('ltp_data_v3.4.0/parser.model')


def segmentor(sentence):
    """
    断词
    :param sentence: 语句
    :return: 词列表
    """""
    global seg
    words = seg.segment(sentence)
    words_list = list(words)
    return words_list


def postagger(words):
    """
    获取词性
    :param words: 词
    :return: 词性
    """
    global post
    pos = post.postag(words)
    pos_list = list(pos)
    return pos_list


def hasSBV(arcs):
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



"""获取文本文件"""
f = open(sys.argv[1])

while True:

    """读一段文本"""
    sentence = f.readline()
    if (sentence is "") or (len(sentence) == 0):
        """ Eof """
        break

    """断句"""
    sents = SentenceSplitter.split(sentence)

    for ss in sents:
        """语句处理"""
        print ss
        words = segmentor(ss)
        # print words
        """
        for _w in words:
            print _w
        """
        pos = postagger(words)
        # print pos
        _idx = 0
        _s = ""
        _cont = False
        for _p in pos:
            if "ws" in _p:
                _s = words[_idx]
                print _s,
            if "n" in _p:
                if not _cont:
                    _s = words[_idx]
                    _cont = True
                else:
                    _s += words[_idx]
            else:
                _cont = False
                if len(_s)>0:
                    print _s,
                    _s = ""
            _idx += 1
        print ""

        """
        netags = list(recognizer.recognize(words, pos))
        print netags
        _idx = 0
        for _n in netags:
            if "Nh" in _n:
                print words[_idx]        
            _idx += 1
        """


parser.release()
post.release()
seg.release()

print("Done.")
