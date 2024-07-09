from py2neo import Graph
# 连接数据库
graph = Graph('http://localhost:7474', username='neo4j', password='123456')

# 执行cql命令
# 删除数据库所有节点和关系
graph.run('match (n) detach delete n')
# 删除标签为phone的所有节点和关系


