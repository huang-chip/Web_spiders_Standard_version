'''
本程序功能为,爬取pixiv排行榜的500个图片的下载链接和图片名
'''
#全局第三方库
import time
import json
import pandas as pd
import requests
import re
#函数声明区域
'''第一步 : 将页面滑动到底端,传递出排行榜页面的源代码'''
def How_to_scroll_pages_till_the_end(url):
    # 函数功能: 虚拟操作浏览器, 一直下滑到底部(可惜的是, 无法观察到页面的每一个元素, 好在pixiv没有使用懒加载, 不影响)
    # 函数I/O参数: [输入: 一个长长页面(通过下滑刷新新元素)的链接(url)];[输出: 整个页面的源代码(Source_code)]
    from selenium import webdriver
    import time
    browser = webdriver.Chrome()
    # 如果你因为没有安装webdriver而导致报错, 请从以下界面找答案(https://zhuanlan.zhihu.com/p/33746246)
    browser.get(url)
    while True:
        hight = 'return document.body.scrollHeight'
        start_height = browser.execute_script(hight)
        # 运行这一行javascript语句, 可以获得整个网页的长度(start_height)
        print("start_height: ",start_height)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        # 上面这行代码的作用是运行javascript语句, 一直向下下拉, 直到拉到底部为止
        time.sleep(5)#给5秒的浏览器缓冲时间,如果5秒后高度不变,则退出循环
        # 如果您网速不好, 请酌情增加上面的sleep值
        end_height = browser.execute_script(hight)
        print("end_height: ", end_height)
        if start_height==end_height:
            # 逻辑:如果我鼠标滚轮滑到底, 和我没滑的时候页面没变, 那我是不是就滑到底了。
            break
    Source_code = browser.page_source
    #源代码太长了,不贴出来了 print(Source_code)
    browser.close()
    return Source_code

'''第二步 : 使用xpath选取方式,将作品编号(id)+作品名字(name)+作者pid整理出来'''
def SelectItems(Source_code):
    # 函数功能: 通过xpath节点解析, 从复杂且长的html中选取我们想要的三个元素, 存为列表输出
    # 函数I/O参数: [输入: pixiv排行榜页面的源代码(Source_code)];[输出: 三个列表(下一行补充)]
    ## 代码块: pic_id_list ,pic_name_list ,author_id_list = SelectItems(Source_code)
    ##   解释:  作品id列表  | 作品原名列表   | 作者pid列表   | = 解析p站源码函数(排行榜源代码)
    from lxml import etree
    html = etree.HTML(Source_code)
    # 'Source_code'是pixiv排行榜页面的'源代码', 上面这行用于初始化xpath
    # 01.下面的xpath是选取整个'排行榜'页面中, 所有'图片(500个)详情页面'的链接
    pic_id = html.xpath("//h2/a/@href")
    ##  说明一下, 图片详情页面不等于图片本体地址
    pic_id_list = []
    for tem0 in pic_id:
        pic_id_list.append(tem0)
    print(pic_id_list) # 格式类似于 "https://www.pixiv.net/artworks/99580753"
    print("选到了", len(pic_id_list), "个图片链接") # 有500个,图片链接可以帮助我们定向原图的详情页
    # 02.下面的xpath是选取(500个)'图片名称'的文本
    pic_name = html.xpath("//h2/a/text()")
    pic_name_list = []
    for tem1 in pic_name:
        pic_name_list.append(tem1)
    print(pic_name_list) #格式类似于 "更新~宵宫"
    print("选到了", len(pic_name_list), "个图片标题") #有500个,图片标题在保存图片时会用到
    # 03.下面的xpath是选取(500个)'作者id'的文本
    author_id = html.xpath("//div[@class='ranking-image-item']//img/@data-user-id")
    author_id_list = []
    for tem1 in author_id:
        author_id_list.append(tem1)
    print(author_id_list)#格式类似于 "58434088"
    print("选到了", len(author_id_list), "个作者id") #有500个,原作者的pid,
    return pic_id_list,pic_name_list,author_id_list
    # 根据图片id和作者id, 可以做些什么?
    # 浏览器访问 https://www.pixiv.net/users/作者pid/artworks 可进入他们的创作主页
    # 浏览器访问 https://www.pixiv.net/artworks/作品id 可进入作品详情页

'''第三步 : 由单个作品的页面得到它的名字和下载链接'''
def get_img_download_url(real_url):
    # (real_url)格式例如: "https://www.pixiv.net/artworks/99528942"
    # 我想你应该能明白这个函数的价值, 他可以夺取到真正的p站图片(如果我再修改一下, 你可以拿这个函数做很多事!)
    # 函数功能: 从单个pixiv作品详情页中, 通过爬虫获取图片真正的地址(由于原图过大, 暂不下载)
    # 函数I/O参数: [输入: pixiv作品详情页链接(real_url)];[输出: 单张图片的 原图地址和图片标题(下一行补充)]
    ## 代码块: str(pic_source[0]),str(pic_title[0]) = get_img_download_url(real_url)
    ##   解释:    原图地址(第1张)  |  图片标题(第1张) | = 解析p站单张图片函数(图片pid页链接)
    import requests
    from lxml import etree
    import re
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        # 请把User-Agent改成自己的,否则会报错
        'referer': 'https://www.pixiv.net',
        # 上面这行代码就是为什么, 你在地址栏输入图片地址却无法访问, 但是我可以的魔法代码~
        "Connection": "close" #此行代码可以跳过SSL证书检验
    }
    requests.packages.urllib3.disable_warnings()#这样就不会看到烦人的报错了
    response = requests.get(real_url,headers=headers,verify=False)
    # 目标网站(real_url)格式例如: "https://www.pixiv.net/artworks/99528942"
    ## (这个链接实际上是一个pixiv插画的详情页面)
    html_text = response.text #源代码获取 - 成功
    html = etree.HTML(html_text)
    pic_title = html.xpath("//title/text()") #图片标题+tag获取 - 成功
    print("爬取到了第:",j+1,"张,选取的图片标题:\t",pic_title[0])
    # pic_source = re.findall('(?<=regular":")\S+(?=\","original)',html_text)
    pic_source = re.findall('(?<=original":")\S+(?=\"},"tags)', html_text) #正则表达式获取原图地址
    print("选取的图片链接:\t",pic_source[0])
    return str(pic_source[0]),str(pic_title[0]) #返回单张图片的 原图地址和图片标题


'''#代码运行区域:'''
# 在2022/08/22更新里面,以下部分做了修改
start_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
print("\t\t程序开始运作", time.strftime('%H:%M:%S', time.localtime(time.time())))#记录一下程序开始的时间
Pixiv_Daily_url = input("请输入pixiv日榜的指定链接(例:https://www.pixiv.net/ranking.php?mode=daily&date=20180819)。\n按回车则爬取本日榜单,请输入:")
# 啊,我为什么要做这么Stupid的输入, 但是我是不会修改这种代码的, 因为他能跑, 气死你, 嘻嘻。
if Pixiv_Daily_url == '' :#这个可以判断input输入了回车
    print("检测到您没有输入, 按照今日pixiv榜单爬取")
    Pixiv_Daily_url = 'https://www.pixiv.net/ranking.php?mode=daily'
print("你输入的是:'",Pixiv_Daily_url,"'")
# 根据url,命名csv的文件名
url_date = Pixiv_Daily_url.split("=")[-1]
if url_date.isdigit()==True:
    csv_filepath = "PixivRank-"+url_date+'.csv'
else:
    import datetime
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    yesterday =yesterday.strftime('%Y%m%d')
    print(yesterday)
    csv_filepath = "PixivRank-" + yesterday + '.csv'
# 上面的if-else只是为了确保, csv文件的名字以当日pixiv排行榜的名字命名, 仅此而已
Source_code = How_to_scroll_pages_till_the_end(Pixiv_Daily_url)#源代码保存完毕
pic_id_list,pic_name_list,author_id_list = SelectItems(Source_code)#选取内容完全成功(图片id样式:'/artworks/99430552')
print("\t\t网页浏览结束", time.strftime('%H:%M:%S', time.localtime(time.time())))#记录一下时间
# folderPath = 'pixiv当日排行前500'
#现在整一个循环!!!
pic_name_list = []#全局变量:作品名字(原名+Tag)
pic_download_list = []#全局变量:作品下载链接
pic_real_id = []#纯净:图片id
'''设计一个双循环,第一个循环确定内循环的开头,可以确定从上次爬取的断点重启,第二个循环进行爬取操作,同时还要兼顾打开列表操作'''
'''第二个循环内置try判断语句,判断语句内由每个图片的页面获取图片下载地址,判断成功后,将数据存入列表,如果报错了就休息十秒继续'''
for j in range(len(pic_download_list),len(pic_id_list)):#这边输入一个图片的页面,开始爬取下载链接等详情信息
    picture_source_html_url = 'https://www.pixiv.net' + pic_id_list[j]
    print("目标网址确定(可能会报错):",picture_source_html_url)
    try:
        pic_source, pic_title = get_img_download_url(picture_source_html_url)#返回单张图片的:原图地址和图片标题(名字+Tag)
    except:
        print("怕太快被ban了喂")
        time.sleep(10)
        j-=1
    ## 防报错的代码
    print("\t\t第",j+1,"张图片,爬取成功时间: ",time.strftime('%H:%M:%S', time.localtime(time.time())))#记录一下时间
    pic_name_list.append(pic_title.split('-')[0])#全局变量:作品名字(原名+Tag)
    pic_download_list.append(pic_source)#全局变量:作品下载链接
    pic_real_id.append(pic_id_list[j].split('/')[-1])#添加了纯净的图片id
    print("添加成功,len分别为{0} , {1}".format(len(pic_name_list),len(pic_download_list)))
# print("pic_name_list:{0},\nlen(pic_name_list):{1}".format())
'''
插入一个列表说明,方便我们理解
# pic_id_list,pic_name_list,author_id_list = SelectItems(Source_code)
  作品id列表  | 作品名字      | 作者pid        [下一行为示例]
  
# pic_source, pic_title = get_img_download_url(picture_source_html_url)
  作品下载地址 | 作品名(tag + 真名 + 作者昵称)   [下一行为示例]
  
我们设计一个字典{"图片原名":pic_name_list[i],"作者pid":author_id_list[i],"作品下载地址":pic_source[i]}
利用循环写入txt吧
'''
print("pic_id_list长度:{0} , pic_name_list长度:{1} , author_id_list长度:{2}, pic_download_list长度:{3}, filepath_list长度:{4}".format(len(pic_id_list),len(pic_name_list),len(author_id_list),len(pic_download_list),len(pic_name_list)))

filepath_list=[]#保存为的文件名
for pic_name,author_id,download_name in zip(pic_name_list,author_id_list,pic_download_list):
    pic_name = str(re.sub('[\/:*?"<>|]','_',pic_name))
    author_id = str(re.sub('[\/:*?"<>|]','_',author_id))
    # 以上两行代码是非常实用的"清除字符串中特殊字符", 可以学习
    filename = 'save_here/' + pic_name + '作者pid' + author_id + '.' + str(download_name.split('.')[-1])
    filepath_list.append(filename)
#字典中的key值即为csv中列名
dataframe = pd.DataFrame({'下载链接':pic_download_list,'保存的文件名':filepath_list})
#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe.to_csv(csv_filepath,index=False,sep=',',encoding='utf-8-sig')
## encoding = 'utf-8-sig'可以完全避免python保存csv时乱码的问题
#至此csv保存成功
print("csv保存成功: ", time.strftime('%H:%M:%S', time.localtime(time.time())))  # 记录一下时间
print("程序开始执行时间为: ",start_time)
'''
呜呜呜不敢相信我真的写完了这个磨人的小妖精, 它的后劲有多大呢? 就是说我把CSDN翻烂了,都找不出爬pixiv的合格代码。
继花了30小时以上时间, 完全自主写完了这一切以后, 成长了很多, 项目代码完全开源(bing找了许多小问题, 感谢大佬们)
'''
"""
第一步 : 将页面滑动到底端,传递出排行榜页面的源代码
第二步 : 使用xpath选取方式,将作品编号(id)+作品名字(name)+作者pid整理出来
第三步 : 由单个作品的页面得到它的名字和下载链接
第四步 : 下载链接可以让我们真正获取到图片原图,图片名+作者pid将会合成图片的名字
详细实现会在后期专门出一期来说道说道捏~大家先看结果吧
"""
