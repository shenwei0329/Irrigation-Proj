# coding: utf-8
#

import mongodb_class
from py2neo import Graph, Node, Relationship

# 图数据库
graph = Graph("bolt://172.16.60.9:7687", username='neo4j', password='NEO4J')

obj_nodes = {}
nodes = {}


def find_object(obj):
    _sql = 'MATCH (n:{}) WHERE n.name="{}" RETURN count(n)'.format(obj['key'], obj['name'])
    _ret = graph.run(_sql).data()
    return _ret[0]['count(n)']


def get_object(obj):
    _sql = 'MATCH (n:{}) WHERE n.name="{}" RETURN n'.format(obj['key'], obj['name'])
    _ret = graph.run(_sql).data()
    return _ret[0]['n']


def add_entity(entity):
    """
    添加一个舆情实体
    """
    global graph, obj_nodes

    # Object
    if find_object({'key': "Object", 'name': entity['Node']}) < 1:
        _node = Node("Object", name=u"%s" % entity['Node'])
    else:
        _node = get_object({'key': "Object", 'name': entity['Node']})

    if entity['Node'] not in obj_nodes:
        obj_nodes[entity['Node']] = _node

    # Add this Event
    if find_object({'key': "Event", 'name': entity['RID']}) < 1:

        _event = Node("Event", name=u"%s" % entity['RID'])
        graph.create(_event)
        # Connect Object with E
        _link = Relationship(obj_nodes[entity['Node']], "ir", _event)
        graph.create(_link)

        print("Add: [{}][{}]".format(entity['Node'], entity['IR_URLTITLE']))
        values = {
            'Date': 'IR_URLTIME',
            'Title': 'IR_URLTITLE',
            'Abstract': 'IR_ABSTRACT',
            'Per': 'SY_PEOPLE',
            'Org': 'SY_ORG',
            'Loc': 'SY_LOC',
            'BB': 'SY_BB_COMMON',
            'Site': 'IR_SITENAME',
            'Url': 'IR_URLNAME',
            'Channel': 'IR_CHANNEL',
            'KeyWord': 'SY_KEYWORDS',
                  }
        for _item in values:

            if _item not in nodes:
                nodes[_item] = {}

            _v = values[_item]
            _key = entity[_v].split(';')
            for _k in _key:

                _k = _k.replace(" ", '')
                if len(_k) == 0:
                    continue
                if _k not in nodes[_item]:
                    print(">\t[{}][{}]".format(_item, _k))
                    _node = Node(_item, name=u"%s" % _k)
                    graph.create(_node)
                    nodes[_item][_k] = _node
                _link = Relationship(_event, _item, nodes[_item][_k])
                graph.create(_link)


def main():

    db = mongodb_class.mongoDB()
    db.connect_db("rivers")

    _sql = {}
    _recs = db.handler("river", "find", _sql)
    for _rec in _recs:
        # print("R: {}".format(_rec))
        if "Node" in _rec:
            add_entity(_rec)


if __name__ == '__main__':
    main()
