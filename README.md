# Flower Knowledge Graph Visualizationa花卉知识图谱可视化

This flower knowledge graph visualization is developed based on neo4j graph database and Django framework for python. I first use python's crawler to crawl the web page data in a structured way, then use py2neo's library and neo4j database to query the data, and finally use echarts.js to visualize the data in the front-end of the web page.
这个花卉知识图谱可视化是基于neo4j图形数据库和python的Django框架开发的。我首先用python的爬虫对网页数控进行结构化的爬取，然后利用py2neo的库和neo4j数据库进行数据的查询，最后用echarts.js在网页前端对数据进行可视化。

# Part 1: crawl the data爬取数据

Step 1：set up neo4j username and password in link_neo4j.py.

Step 2: Run crawler.py to crawl the URL "http://www.aihuhua.com/hua/". The crawled data will be in the data folder, which I zipped and uploaded.

# Part 2：create the knowledge graph构建知识图谱

use the createKG.py file to import the data to neo4j

# Part 3：visualize the data数据可视化

set the configutation of the Django frame

design the front-end webite
![image](https://github.com/Becky-Dai/Flower-Knowledge-Graph-Visualization/assets/58799631/a404331a-afcc-4bf6-94f2-36bc7e33abc0)

complete the query function 

visualize the retun data

