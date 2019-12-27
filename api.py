# -*- coding:UTF-8 -*-
#

from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from pyltp import SentenceSplitter
from pyltp import NamedEntityRecognizer
import re

from flask import Flask, jsonify
from flask import request

import logging

seg = Segmentor()
seg.load_with_lexicon('ltp_data_v3.4.0/cws.model', './ext_word_cloud')
post = Postagger()
# post.load_with_lexicon('ltp_data_v3.4.0/pos.model', './ext_word_cloud')
post.load('ltp_data_v3.4.0/pos.model')
recognizer = NamedEntityRecognizer()
recognizer.load('ltp_data_v3.4.0/ner.model')
parser = Parser()
parser.load('ltp_data_v3.4.0/parser.model')

app = Flask(__name__)

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


@app.route('/api/v1.0/ltps', methods=['POST'])
def create_ltp():
    """
    cmd: [] in 'seg' OR 'pos', 'recog', 'parser'
    """

    if not request.json or not 'text' in request.json or not 'cmd' in request.json:
        abort(400)

    _text = (request.json['text']).encode('utf-8')
    _cmd = request.json['cmd']

    if "log" in _cmd:
        print(_text)
        return jsonify({'ltp': "OK"}), 201

    sentence = _text.replace("‘", "").replace("’", "").replace("”", "").replace("“", "")
    sents = SentenceSplitter.split(sentence)
    if "seg" in _cmd:
        _s = []
        for __s in sents:
            _s.append(__s)
        return jsonify({'ltp': _s}), 201

    _sentences = []
    for _ss in sents:

        words = segmentor(_ss)
        pos = postagger(words)

        context = {}
        context["words"] = words
        for _c in _cmd:
            if "pos" in _c:
                context[_c] = pos
            elif "recog" in _c:
                _rec = list(recognizer.recognize(words, pos))
                context[_c] = _rec
            elif "pars" in _c:
                arcs = parser.parse(words, pos)
                _pars = []
                _idx = 1
                for arc in arcs:
                    _pars.append((arc.head, _idx, arc.relation, words[_idx-1]))
                    _idx += 1
                context[_c] = _pars
                """
                rely_id = [arc.head for arc in arcs]  # 提取依存父节点id
                relation = [arc.relation for arc in arcs]  # 提取依存关系
                heads = ['Root' if id == 0 else words[id-1] for id in rely_id]  # 匹配依存父节点词语

                for i in range(len(words)):
                    context[_c].append((relation[i], words[i], heads[i]))
                """
        _sentences.append(context)

    return jsonify({'ltp': _sentences}), 201

if __name__ == '__main__':

    hdl = logging.FileHandler('api.log', encoding='UTF-8')
    hdl.setLevel(logging.DEBUG)
    app.logger.addHandler(hdl)

    app.run(host="0.0.0.0", port=8181, debug=False)


"""
parser.release()
post.release()
"""
#
