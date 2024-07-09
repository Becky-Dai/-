# Flower Knowledge Graph Visualizationa 花卉知识图谱可视化

This flower knowledge graph visualization is developed based on neo4j graph database and Django framework for python. I first use python's crawler to crawl the web page data in a structured way, then use py2neo's library and neo4j database to query the data, and finally use echarts.js to visualize the data in the front-end of the web page.

这个花卉知识图谱可视化是基于neo4j图形数据库和python的Django框架开发的。我首先用python的爬虫对网页数控进行结构化的爬取，然后利用py2neo的库和neo4j数据库进行数据的查询，最后用echarts.js在网页前端对数据进行可视化。

# Part 1: crawl the data 爬取数据

Step 1：set up neo4j username and password in link_neo4j.py.

Step 2: Run crawler.py to crawl the URL "http://www.aihuhua.com/hua/". The crawled data will be in the data folder, which I zipped and uploaded.

# Part 2：create the knowledge graph 构建知识图谱

use the createKG.py file to import the data to neo4j

# Part 3：visualize the data 数据可视化

set the configutation of the Django frame 设置好Django框架

design the front-end webite 前端设计

![image](https://github.com/Becky-Dai/Flower-Knowledge-Graph-Visualization/assets/58799631/a404331a-afcc-4bf6-94f2-36bc7e33abc0)

![image](https://github.com/Becky-Dai/Flower-Knowledge-Graph-Visualization/assets/58799631/9c32d138-12ca-4e45-8204-a27405965d31)

![image](https://github.com/Becky-Dai/Flower-Knowledge-Graph-Visualization/assets/58799631/cbd53438-16df-44cd-863a-8aa5b46bf569)

complete the query function and visualize the retun data 完成查询功能和可视化返回的数据

Enter the name of the entity node in the search box and click Search. 在搜索框输入实体节点的名称，点击搜索

The backend search code can be found in my Django_web/query_function path! 后端的搜索代码可以在我的Django_web/query_function路径下可以找到！

![image](https://github.com/Becky-Dai/Flower-Knowledge-Graph-Visualization/assets/58799631/7e2097a9-25a4-4545-9494-065b97f4ce4f)

The front-end will return the knowledge graph rendered by echats.js, and these settings are available in my Django_web/templates path. 前端将会返回echats.js渲染的知识图谱，而这些设置均在我的Django_web/templates路径下可以找到

![image](https://github.com/Becky-Dai/Flower-Knowledge-Graph-Visualization/assets/58799631/d63b8f4d-df52-4573-b76f-ad8eda9bf0e1)


![image](https://github.com/Becky-Dai/Flower-Knowledge-Graph-Visualization/assets/58799631/32f96024-8d67-47fc-88c9-8bfd46467780)

![image](https://github.com/Becky-Dai/Flower-Knowledge-Graph-Visualization/assets/58799631/a0744a35-4943-4db4-98d9-0fd756f98242)




