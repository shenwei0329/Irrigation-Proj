#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os

# ROOTDIR = os.path.join(os.path.dirname(__file__), os.pardir)
ROOTDIR = '.'
# sys.path = [os.path.join(ROOTDIR, "lib")] + sys.path

# Set your own model path
MODELDIR=os.path.join(ROOTDIR, "ltp_data_v3.4.0")

from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

# paragraph = '中国进出口银行与中国银行加强合作。一切反动派都是纸老虎！'
# paragraph = '马克思主义者认为人类的生产活动是最基本的实践活动，是决定其他一切活动的东西，人的认识，主要地依赖于物质的生产活动，逐渐地了解自然的现象、自然的性质、自然的规律性、人和自然的关系；而且经过生产活动，也在各种不同程度上逐渐地认识了人和人的一定的相互关系。'
paragraph = '举例来说．9．1l恐怖事件就是由一群有共同目的的人在长期互动的过程中产生的极化效应造成的。国家研究委员会的专家称。成为一个恐怖分子的过程可能就是把个体和其他信念系统隔离开，使潜在的目标失去人性，而且令其不能忍受任何异议(Smelser&Mitchell，2002)。麦若瑞(Anel MeraIj，2002)是一位中东和斯里兰卡自杀性恐怖主义的研究者．他认为制造自杀性恐怖事件的关键因素就是群体过程。“据我所知，还从未出现过因个人一时的兴致而导致的自杀性事件。”大屠杀都是杀人者相互怂恿而造成的团体现象(zaiOBC·，2000)。'

sentence = SentenceSplitter.split(paragraph)[0]

segmentor = Segmentor()
print MODELDIR
segmentor.load(os.path.join(MODELDIR, "cws.model"))
words = segmentor.segment(sentence)
print("\t".join(words))

postagger = Postagger()
postagger.load(os.path.join(MODELDIR, "pos.model"))
postags = postagger.postag(words)
# list-of-string parameter is support in 0.1.5
# postags = postagger.postag(["中国","进出口","银行","与","中国银行","加强","合作"])
print("\t".join(postags))

parser = Parser()
parser.load(os.path.join(MODELDIR, "parser.model"))
arcs = parser.parse(words, postags)

print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

recognizer = NamedEntityRecognizer()
recognizer.load(os.path.join(MODELDIR, "ner.model"))
netags = recognizer.recognize(words, postags)
print("\t".join(netags))

labeller = SementicRoleLabeller()
labeller.load(os.path.join(MODELDIR, "pisrl.model"))
roles = labeller.label(words, postags, arcs)

for role in roles:
    print(role.index, "".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

segmentor.release()
postagger.release()
parser.release()
recognizer.release()
labeller.release()

