# Web_spiders_Standard_version
这里保存着所有可以稳定运行的爬虫项目   
Index:   
|--**bing搜索引擎爬虫** (待完成,正在调试UI界面)  
|--**随机一文-短篇小说生成+朗读器** (100%完成)
|--**pixiv排行榜爬取v1.0** (100%完成,可运行) (v2.0已设计好)

# Git操作的坑
每次项目发生改动前:
```Git
git pull
# 这样可以将远程仓库及时同步到本地
```
**每次提交项目标准操作**  
```Git
git add .
git commit -m "写一些备注"
git push 
# 这样可以将远程仓库及时同步到本地
```
# 报错时应对方案
```shell
# 在git push操作时, 报错信息:
# "fatal: unable to access 'https://github.com/huang-chip/Web_spiders_Standard_version.git/': OpenSSL SSL_read: Connection was reset, errno 10054"
# 解决方案
git config --global http. ssl Verify “false”
# 原理: 既然是SSL证书错误, 那么我们直接改变git设置, 取消SSL证书审核机制即可
```
---
按理来讲,2022/8/6-00:45
应该有一个新的文件夹被上传的, 但是没有(悲)  
(发生此次错误的原因是:没有*git push*)
