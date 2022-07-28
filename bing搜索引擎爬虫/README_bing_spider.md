# BING_spider (Standard_version)
---
<!-- <center><h1>中文介绍</h1></center> -->

## 运行环境(python3.0版本以上)和所需的第三方库
- [x] requests库 (爬虫最基础的请求库)
- [x] lxml库 (爬虫解析库, 用于对HTML的解析)
- [x] xlrd库 (excel文档读取)
- [x] xlwt库 (excel文档写入)

## 产品所实现的功能一览
1. 由excel或txt,批量存储关键词  
2. 由xlrd批量读入关键词存放为列表  
3. 批量读入关键词, 将每一个关键词合成为网站url  
4. 用requests库得到从第一页到第十页的源代码, 拼接为一个总的html  
5. 用lxml得到节点内容(标题,源地址)
6. 用xlwt存入excel。
<center><p>流程图如下</p></center>
<!-- 反正没人看见, 向晚是一块木头(嘻嘻) -->

[![ZwNEX0.png](https://www.helloimg.com/images/2022/07/28/ZwNEX0.png)](https://www.helloimg.com/image/ZwNEX0)
