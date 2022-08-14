'''
|           标题            - 匚 X  |
|   选择excel文件 : ____________    |
|   or选择txt文件 : ____________    | (二选一,先选哪一类文件,然后显示输入框)
|   需要哪些元素? 多选框   匚         |
|   需要多少页的数据? 输入框  匚__     |
|   删除不要的数据 : 选择停用词txt     |
|   进度条.....                     |
'''
import tkinter as tk




def select_keyword_file(): #这里绑定"选择"按钮
    keyword_file_path.set(filedialog.askopenfilename(title="选择存储关键词的文件", initialdir="."))
    read_keyword_return_list()

def select_stopwords_file(): #这里绑定"选择停用词"按钮
    stopwords_file_path.set(filedialog.askopenfilename(title="选择停用词文件", initialdir="."))

def read_keyword_return_list(): #函数的功能为,从输入框中得到文件名, 将一个可变变量(关键字)输入文本框, 同时返回一个列表(原始url)
    keyword_file_name = keyword_file_path.get()
    if keyword_file_name.split('.')[-1] == 'txt':
        print("文件类型读取成功,开始读取文件")
        keywords_list = []
        keywords_in_var = []
        with open(keyword_file_name, 'r', encoding='utf-8') as fp:
            txt_content = fp.readlines()  # 将每一行保存为一个列表元素
            for line in txt_content:
                each_keyword = line.replace("\n", "")
                keywords_in_var.append(each_keyword)  # 可变变量只放关键词
                url = 'https://cn.bing.com/search?q=' + each_keyword
                keywords_list.append(url)  # 真正的url都放在return的列表中
        print(keywords_list, "\n", len(keywords_list))
        Var_For_KeywordsUrl_List.set(keywords_in_var)
        keyword_textbox.insert("end", Var_For_KeywordsUrl_List.get()) # 将所有关键词显示在文字框中
        return keywords_list
        #值得注意,列表keywords_list里面存放关键字的原初url,可以全局调用
    else:
        print('文件名错了,请选择.txt格式的文件')


def StartSpy():#这里绑定的是"开始爬取"按钮
    keyword_textbox.delete("1.0","end")#首先把文本框里面的第一个值到最后一个值删除
    keywords_list = read_keyword_return_list()# keywords_list里面是所有原始链接的列表, 我们需要的是爬取这个链接, 每次爬取后重新定向Url
    progressbarOne['maximum'] = len(keywords_list) #所有关键词的长度为进度条1的长度
    for OriginUrl in keywords_list:
        print(OriginUrl)
        # 对原始链接进行两个操作, 1. requests爬取 2. lxml分析源代码并存入目标列表 3.判断"下一页"的链接是否存在在集合中, 是则退出循环, 否则爬取下一页中信息
        NewsTitle_List=[]
        NewsLink_List=[]
        NewsAbstract_List=[]
        Now_keyword.set(OriginUrl.split("=")[-1])
        progressbarOne['value'] += 1
        # url = OriginUrl
        #对每一个关键词进行以下循环操作
        for page in range(0,100,10):
            progressbarTwo['value'] = page
            window.update()
            url = OriginUrl + '&first='+ str(page+1)
            print("我们目标的网站是",url)
            Resource_Code = get_one_page(url)
            new_NewsTitle_List, new_NewsLink_List, new_NewsAbstract_List = Select_lxml(Resource_Code)
            for title0,link0,abstract0 in zip(new_NewsTitle_List, new_NewsLink_List, new_NewsAbstract_List):
                NewsTitle_List.append(title0)
                NewsLink_List.append(link0)
                NewsAbstract_List.append(abstract0)
        import pandas as pd
        filename = OriginUrl.split("=")[-1]+'-必应网页汇总.xlsx'
        data = {'关键词': OriginUrl.split("=")[-1],'网页标题': NewsTitle_List, '网页链接': NewsLink_List, '网页详情': NewsAbstract_List}
        df1 = pd.DataFrame(data)
        df1.to_excel(filename, sheet_name='Sheet1', index=True)
        # 说一下思路, 首先获取源代码,取标题,链接,简介,存在结构体中,
        # 然后,找到"title=下一页",用正则提取出其中的"&first=101",经过比对加到下一组url中,如果和集合中一模一样,则选取元素后跳出循环
        progressbarTwo['value'] +=10 #这个可以使最后一个关键词爬取完毕后, 进度条填满

def get_one_page(url):#这是一个通用函数, 输入一个网页, 返回其源代码
    import requests
    import time
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        # 'Cookie': '_EDGE_V=1; MUID=23E68497FBCA6D5336429442FA186C48; MUIDB=23E68497FBCA6D5336429442FA186C48; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=1110198E704D49E6BB43FAD45FD394A2&dmnchg=1; MUIDV=NU=1; ANON=A=EA01BF5C569E5109ADB08E63FFFFFFFF&E=1a2e&W=1; NAP=V=1.9&E=19d4&C=n-o83IrB4U07LopXmvLrFaCUA2QwkLaXf_hs9TICIM4D1ZJtI8tPJQ&W=1; PPLState=1; _ITAB=STAB=TR; _tarLang=default=zh-Hans; _TTSS_OUT=hist=WyJlbiIsInpoLUhhbnMiXQ==; _TTSS_IN=hist=WyJlbiIsInpoLUhhbnMiLCJhdXRvLWRldGVjdCJd; KievRPSSecAuth=FABSBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACGnV4HNRGLRHEAQCnY5RD3dyn9vsQhRwH/XLVt3Err7wzhuIqxa/vBJ1e/7MUEmlNOdFwW1GKazHt1t7FIUEUW7SQ/4UoV+CiLMF8MQR5VcAsHZjeG8D8picQb2FMOhNPxdLhsL29a00Vugq7jivk6XXr2s1jQ04zmJAkIAWHzh4GPRSlBwE/ZecZ5AmyLqAL8p8YZ9MyRiK9CfmqC8TWnxeoKLlXBzVdp3Kntt8OyMTSiXvKXTFo/kw9zri4Rr53taB7o+bG44lGDKIdt9k4buQtClFxXH9BFsK9hF2rqd9gYAb42JI3aX3NCkVIRCZYtqoxqz7ZJX36n/rkASNXZacwxjbF6drrxstgk6EaTVFUec91U+jH/eNKi9WbT8iAy63pjUiDRb9dJzgjVWz8pVcbWitDAb3X8vBZ9cMn50m4bk8Ic6RRJ+sg2USyVt+sHZMTXOitl1rybqgEHsm5plQX1q3XXLuWlpdnwqEQMAT7EfFt4wu9qOB4XizmPPqbXrdZuqRjYT2jLvne79YnhbtDZKUzrRyH+yfrhH8gHFpqXRVjQuJWxqSkrHx1TBoO9Uztq6Or8YW7Vl4X2exKc3JWhPgKV5JN7XS3agMQvlbQvxtGjAke6FZwftnSlzTwDhDosbYNc1ZYCuE3r2970cLjgfZJ3SFTkGdJAqPVVXBX9JQkiPMd5vKo8UstmXs2pW9yEKfjaHU8SNnlG9iW6ocHr06gdTD407mSwDHyqTZf4WYct6K3JU6rEO2U+32QgA6Q2jGtbAhyFoRR6xrN+pkqXKGp9qG8FNbhAN/0PJLo4MUmdMhlCDarUMeFbEQuFshj3c6PNwhP5xuz+CvjBhRRDZJLyOkIBkFYr/4PMFk6XnClHg2uOuBpsz3yDcFXkcCsZoQQv174CjViZkLFIUPr00N5bVbCDhMQ95wTo4Ptv/s0VT1ugVJUmoIGgtVQK3RjEBiH7nZg/E2Vo16zyTZtXglbeHm5KEup4YeEniQv0ga2OZn9JX9Cq6tPll3mlWCIkqoL33SQ++j+C7TDYWWEyQtJaoUFHsemVch2jjJepYstFz5FA2ZZIQADSI16rKYVet9kl2Itst/6Vcuk6GYjzUdAt3QSGFRIxHxRYfVXIbE+2dzBB83JcuLfq0pK0rShIQaCM6DsBUjGQ5ZuI9eGpP2IM1tBQ+/Uxxkt0/fGhmKsw1gDbvivFoWjauQM/2wmQ6ZEbiPvLEHt/DdHr8WI5avulB4oMhG88G2m6WdV+5n2W9uSsFsRBNuDMKM7gGAVOF0u3hacIklYxmA63D2QhpCE+5KcS6ervv+8EOEYXJA5w7XXfgAsrIMA8F5v8tLGpTECkVeYGDAR2cBKnP3m+3SX+77yfBgX41ImCQYYcltbWr0lEbSSxQAfg6U8UHiEIn3k1a4gBZWr2mE1kg=; _U=1zj1Y2CeHphfQ59w6ndZh7q5MCkL1DTv6HAfUxUIg-xSCtnxT3qmP8a8pYrkTBQnwIdsVfISUkDIpGKxoKmkdZ2gm0__9bB896jfIiE_gjgZjhGA4fDpaUn2mti90rCCAdqeJe_bmIBUNCpWy4BejEvwzbCPbAuRS4seMMGiOlykQFNi0b30DGw4lkXFghPySuALvfUvdFfvQtpFz2zT8ww; WLID=jLfLUpC9C0JOTleFPc1cVbHcEUK833rth2Nm3S47ibwoSWD4xlEXUK9iu+MfI2wI6K6Z2Ztrtlh5QB2x2zIJY2YHycUDJx2aDfZDM5LNFac=; ABDEF=V=13&ABDV=11&MRNB=1639282241480&MRB=0; imgv=lodlg=1; SUID=A; _EDGE_S=SID=24E3815EC7366FE82633904FC6186EB6; WLS=C=7c17b8fa1e6c1ada&N=%e9%91%ab%e8%bf%9c; _SS=SID=24E3815EC7366FE82633904FC6186EB6; SRCHUSR=DOB=20211019&T=1639805383000&TPC=1639805393000&POEX=W; ipv6=hit=1639808994830&t=4; _HPVN=CS=eyJQbiI6eyJDbiI6NTcsIlN0IjoyLCJRcyI6MCwiUHJvZCI6IlAifSwiU2MiOnsiQ24iOjU3LCJTdCI6MCwiUXMiOjAsIlByb2QiOiJIIn0sIlF6Ijp7IkNuIjo1NywiU3QiOjEsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMS0xMi0xOFQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6NTIxfQ==; SNRHOP=I=&TS=; SRCHHPGUSR=SRCHLANG=zh-Hans&BRW=NOTP&BRH=M&CW=686&CH=778&SW=1596&SH=998&DPR=1.7645833492279053&UTC=480&DM=0&HV=1639805465&BZA=0&WTS=63774486570'
    }
    response = requests.get(url, headers=headers, timeout=10)
    time.sleep(1)
    if response.status_code == 200:
        return response.text
    else:
        print("爬取结果出现错误")
        return None

def Select_lxml(Resource_Code):
    from lxml import etree
    NewsTitle_List=[]
    NewsLink_List=[]
    NewsAbstract_List=[]
    # 以上是原始数据初始化领域
    html = etree.HTML(Resource_Code)
    result = etree.tostring(html)
    result = result.decode('utf-8')
    # 这三行代码, 首先将字符串初始化为一个XPath解析对象, tostring()方法会补全修正后的代码, 用decode方法将bytes型转为str型
    Big_div_list = html.xpath('//div[@id="b_content"]//ol[@id="b_results"]/li[@class="b_algo"]')  # 里面包含了所有标题以及简介
    print("----div_list,指向包含一切元素的‘b_algo’(长度为)：", len(Big_div_list))
    title_content = Big_div_list[0].xpath('//div[@class="b_title"]/h2/a')
    for temp0 in title_content:#原来这个byd是可以遍历的啊
        Each_NewsTitle = temp0.xpath('string(.)')
        Each_NewsLink = temp0.xpath('@href')
        NewsTitle_List.append(Each_NewsTitle)
        NewsLink_List.append(Each_NewsLink)
        print(Each_NewsTitle)#自动拼接节点内的所有字符(草!这个方法真的tmd好用!)
        print(Each_NewsLink)
    title_abstract = Big_div_list[0].xpath('//div[@class="b_caption"]/p')
    for temp1 in title_abstract:
        Each_NewsAbstract = temp1.xpath('string(.)')
        NewsAbstract_List.append(Each_NewsAbstract)
        print(Each_NewsAbstract)

    return NewsTitle_List, NewsLink_List, NewsAbstract_List


'''UI设计区域'''
import tkinter as tk
import tkinter.ttk
import tkinter.filedialog as filedialog
window = tk.Tk()
window.title("必应搜索引擎-自定义爬虫")
keyword_file_path = tk.StringVar()
Var_For_KeywordsUrl_List = tk.StringVar()
stopwords_file_path = tk.StringVar()
Now_keyword = tk.StringVar()

lbl_file = tk.Label(window, text='选取关键词文件(.xls或.txt) : ')
lbl_file.grid(row=0, column=0,columnspan=3)

txt_file = tk.Entry(window, width=80, textvariable=keyword_file_path)
txt_file.grid(row=0, column=3, sticky=tk.W)

btn_file = tk.Button(window, text="选择", command=select_keyword_file)#<--这里有函数,
# 点击"选择"会返回一个文件名的可变变量, entry获取到文件名,会判断文件是否为txt文件,
# 如果是, 在textarea里面会显示txt中每一个关键字(关键字必须一行一个, 否则无效)
# 并且会生成一个列表:keywords_list(可全局调用),里面存储着所有关键字的原初数据,例如:
## ['https://cn.bing.com/search?q=嘉然', 'https://cn.bing.com/search?q=向晚', 'https://cn.bing.com/search?q=奶琳', 'https://cn.bing.com/search?q=贝拉', 'https://cn.bing.com/search?q=伽乐']
btn_file.grid(row=0, column=4, sticky=tk.E+tk.W)

show_file_lbl = tk.Label(window, text='请确认关键词:')
show_file_lbl.grid(row=1, column=0,columnspan=2)

keyword_textbox = tk.Text(window, height=4)
keyword_textbox.grid(row=1, column=2, columnspan=2, sticky=tk.W + tk.E)

btn_start_spy = tk.Button(window, text="开始爬取", command=StartSpy, height=2)
btn_start_spy.grid(row=1, column=4, sticky=tk.E)

lbl_loading_keywords = tk.Label(window, text='关键词进度:')
lbl_loading_keywords.grid(row=2, column=0, columnspan=2)

progressbarOne = tkinter.ttk.Progressbar(window, length=500)
progressbarOne.grid(row=2, column=2, columnspan=2, sticky=tk.W)

# lbl_declaration = tk.Label(window, text='', bg='#12a182')
# lbl_declaration.grid(row=2, column=2, columnspan=2)

lbl_loading_eachwords = tk.Label(window, textvariable=Now_keyword)
lbl_loading_eachwords.grid(row=2, column=3, sticky=tk.E)

progressbarTwo = tkinter.ttk.Progressbar(window,value=0,length=50)
progressbarTwo.grid(row=2, column=4)

# frame01 = tk.Frame(window)
# frame01.grid(row=2, column=0,  columnspan=3, sticky=tk.E+tk.W)
#
# lbl_select_num = tk.Label(frame01, text='页数:')
# lbl_select_num.grid(row=0, column=0)
#
# select_num_bar = tk.Scale(frame01, from_=1,to=15,orient=tk.HORIZONTAL)
# select_num_bar.grid(row=0, column=1)
#
# lbl_stopwords_file = tk.Label(frame01, text='选取停用词文件(.txt) : ')
# lbl_stopwords_file.grid(row=0, column=2)
#
# entry_stopwords_file = tk.Entry(frame01, width=80, textvariable=stopwords_file_path)
# entry_stopwords_file.grid(row=0, column=3, sticky=tk.W)
#
# btn_stopwords_file = tk.Button(frame01, text="选择停用词", command=select_stopwords_file)
# btn_stopwords_file.grid(row=0, column=4)

window.mainloop()
