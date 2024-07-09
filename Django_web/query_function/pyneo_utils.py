from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher

color = {
    "花卉大全": "#5470c6",
    "花卉": "#ee6666",
    "花卉品种": "#91cc75",
    "花卉功能": "#73c0de",
    "应用环境": "#fac858",
    "other": "#73c0de"
}


def get_node_by_name(g, node_type, name):
    # g=Graph('http://localhost:7474',user='neo4j',password='123')
    matcher = NodeMatcher(g)
    endnode = matcher.match(node_type, name=name).first()
    print(endnode)
    if endnode != None:
        return endnode
    else:
        return None


def get_str_by_dict(mydict):
    last = ""
    print(mydict)
    print(type(mydict))
    for key in mydict:
        last = str(key) + ":" + str(mydict[key]) + "<br>" + last
    return last


def get_all_relation(start, relation, end):
    datas = []
    links = []
    cache = []
    categories = []
    legend_data = []
    g = Graph('http://localhost:7474', user='neo4j', password='123456')
    sql = "MATCH (n)-[%s]-(b) %s RETURN n,r,b limit 100"
    mn = ""
    mr = ""
    mb = ""
    param = ""
    if start != "":
        param = "where n.name='" + start + "'"
    if relation == "":
        mr = "r"
    else:
        mr = "r:" + relation
    if end != "":
        if "where" in param:
            param = param + " and b.name='" + end + "'"
        else:
            param = "where b.name='" + end + "'"

    sql = sql % (mr, param)
    print(sql)
    # if name == "":
    #     nodes_data_all = g.run("MATCH (n)-[r]-(b) RETURN n,r,b limit 100").data()
    # else:
    nodes_data_all = g.run(sql).data()
    for nodes_relations in nodes_data_all:
        print("----")
        start_lable = str(nodes_relations['n'].labels).replace(":", "")
        end_lable = str(nodes_relations['b'].labels).replace(":", "")
        start = dict(nodes_relations['n'])
        end = dict(nodes_relations['b'])
        relation = "relation"
        if "name" not in start or "name" not in end:
            continue
        start_name = start["name"]
        end_name = end["name"]
        try:
            relation = str(nodes_relations['r'].keys).split(" ")[4]
        except Exception as e:
            print(e)
            continue
        if start_name not in cache:
            if start_lable in color:
                datas.append(
                    {"name": start_name, "attr": start, "color": color[start_lable], "des": get_str_by_dict(start),
                     "category": start_lable})
            else:
                datas.append({"name": start_name, "attr": start, "color": color["other"], "des": get_str_by_dict(start),
                              "category": start_lable})
            cache.append(start_name)
        if end_name not in cache:
            if end_lable in color:
                datas.append({"name": end_name, "attr": end, "color": color[end_lable], "des": get_str_by_dict(end),
                              "category": end_lable})
            else:
                datas.append({"name": end_name, "attr": end, "color": color["other"], "des": get_str_by_dict(end),
                              "category": end_lable})
            cache.append(end_name)

        if start_lable not in legend_data:
            legend_data.append(start_lable)
            categories.append({"name": start_lable})
        if end_lable not in legend_data:
            legend_data.append(end_lable)
            categories.append({"name": end_lable})

        cache_relation = start_name + "-" + end_name
        if cache_relation not in cache:
            links.append(
                {
                    "source": start_name,
                    "target": end_name,
                    "name": relation
                }
            )
            cache.append(cache_relation)
    print("=====")
    print(datas)
    print(links)

    return {"datas": datas, "links": links, "legend_data": legend_data, "categories": categories}


def get_legal_type_relation(legal_type, start, relation, end):
    datas = []
    links = []
    cache = []
    categories = []
    legend_data = []
    g = Graph('http://localhost:7474', user='neo4j', password='123456')
    "where n.name='%s' and b.name='%s'"
    sql = "MATCH (n:legalType)-[r]->(b:legal) %s RETURN n,r,b limit 100"
    mn = ""
    mb = ""
    param = ""
    if start != "":
        if "where" not in param:
            param = "where b.name='" + start + "' "
        else:
            param = param + " and b.name='" + start + "'"
    if legal_type != "":
        if "where" not in param:
            param = "where n.name='" + legal_type + "' "
        else:
            param = param + " and n.name='" + legal_type + "'"

    sql = sql % (param)
    print(sql)
    # if name == "":
    #     nodes_data_all = g.run("MATCH (n)-[r]-(b) RETURN n,r,b limit 100").data()
    # else:
    nodes_data_all = g.run(sql).data()
    for nodes_relations in nodes_data_all:
        print("----")
        start_lable = str(nodes_relations['n'].labels).replace(":", "")
        end_lable = str(nodes_relations['b'].labels).replace(":", "")
        start = dict(nodes_relations['n'])
        end = dict(nodes_relations['b'])
        relation = "relation"
        if "name" not in start or "name" not in end:
            continue
        start_name = start["name"]
        end_name = end["name"]
        try:
            relation = str(nodes_relations['r'].keys).split(" ")[4]
        except Exception as e:
            print(e)
            continue
        if start_name not in cache:
            if start_lable in color:
                datas.append(
                    {"name": start_name, "attr": start, "color": color[start_lable], "des": get_str_by_dict(start),
                     "category": start_lable})
            else:
                datas.append({"name": start_name, "attr": start, "color": color["other"], "des": get_str_by_dict(start),
                              "category": start_lable})
            cache.append(start_name)
        if end_name not in cache:
            if end_lable in color:
                datas.append({"name": end_name, "attr": end, "color": color[end_lable], "des": get_str_by_dict(end),
                              "category": end_lable})
            else:
                datas.append({"name": end_name, "attr": end, "color": color["other"], "des": get_str_by_dict(end),
                              "category": end_lable})
            cache.append(end_name)

        if start_lable not in legend_data:
            legend_data.append(start_lable)
            categories.append({"name": start_lable})
        if end_lable not in legend_data:
            legend_data.append(end_lable)
            categories.append({"name": end_lable})

        cache_relation = start_name + "-" + end_name
        if cache_relation not in cache:
            links.append(
                {
                    "source": start_name,
                    "target": end_name,
                    "name": relation
                }
            )
            cache.append(cache_relation)
    print("=====")
    print(datas)
    print(links)

    return {"datas": datas, "links": links, "legend_data": legend_data, "categories": categories}
