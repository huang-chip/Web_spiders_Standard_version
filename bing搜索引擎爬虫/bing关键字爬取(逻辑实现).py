import xlrd
import xlwt
import requests
from lxml import etree
import random
import time


def read_by_excel():  # 从指定文件里面取出一整列结果
    book = xlrd.open_workbook('data.xlsx')
    sheet1 = book.sheets()[0]
    all_keywords = sheet1.col_values(1)
    return all_keywords


def output_url(keywords):
    keywords
    url = "https://cn.bing.com/search?q=" + keywords
    return url


def changepage(url, total_page):
    real_url_list = []
    for i in range(total_page):
        j = i * 10 + 1
        each_url = url + '&first=' + str(j)
        real_url_list.append(each_url)
    return real_url_list


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Cookie': '_EDGE_V=1; MUID=23E68497FBCA6D5336429442FA186C48; MUIDB=23E68497FBCA6D5336429442FA186C48; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=1110198E704D49E6BB43FAD45FD394A2&dmnchg=1; MUIDV=NU=1; ANON=A=EA01BF5C569E5109ADB08E63FFFFFFFF&E=1a2e&W=1; NAP=V=1.9&E=19d4&C=n-o83IrB4U07LopXmvLrFaCUA2QwkLaXf_hs9TICIM4D1ZJtI8tPJQ&W=1; PPLState=1; _ITAB=STAB=TR; _tarLang=default=zh-Hans; _TTSS_OUT=hist=WyJlbiIsInpoLUhhbnMiXQ==; _TTSS_IN=hist=WyJlbiIsInpoLUhhbnMiLCJhdXRvLWRldGVjdCJd; KievRPSSecAuth=FABSBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACGnV4HNRGLRHEAQCnY5RD3dyn9vsQhRwH/XLVt3Err7wzhuIqxa/vBJ1e/7MUEmlNOdFwW1GKazHt1t7FIUEUW7SQ/4UoV+CiLMF8MQR5VcAsHZjeG8D8picQb2FMOhNPxdLhsL29a00Vugq7jivk6XXr2s1jQ04zmJAkIAWHzh4GPRSlBwE/ZecZ5AmyLqAL8p8YZ9MyRiK9CfmqC8TWnxeoKLlXBzVdp3Kntt8OyMTSiXvKXTFo/kw9zri4Rr53taB7o+bG44lGDKIdt9k4buQtClFxXH9BFsK9hF2rqd9gYAb42JI3aX3NCkVIRCZYtqoxqz7ZJX36n/rkASNXZacwxjbF6drrxstgk6EaTVFUec91U+jH/eNKi9WbT8iAy63pjUiDRb9dJzgjVWz8pVcbWitDAb3X8vBZ9cMn50m4bk8Ic6RRJ+sg2USyVt+sHZMTXOitl1rybqgEHsm5plQX1q3XXLuWlpdnwqEQMAT7EfFt4wu9qOB4XizmPPqbXrdZuqRjYT2jLvne79YnhbtDZKUzrRyH+yfrhH8gHFpqXRVjQuJWxqSkrHx1TBoO9Uztq6Or8YW7Vl4X2exKc3JWhPgKV5JN7XS3agMQvlbQvxtGjAke6FZwftnSlzTwDhDosbYNc1ZYCuE3r2970cLjgfZJ3SFTkGdJAqPVVXBX9JQkiPMd5vKo8UstmXs2pW9yEKfjaHU8SNnlG9iW6ocHr06gdTD407mSwDHyqTZf4WYct6K3JU6rEO2U+32QgA6Q2jGtbAhyFoRR6xrN+pkqXKGp9qG8FNbhAN/0PJLo4MUmdMhlCDarUMeFbEQuFshj3c6PNwhP5xuz+CvjBhRRDZJLyOkIBkFYr/4PMFk6XnClHg2uOuBpsz3yDcFXkcCsZoQQv174CjViZkLFIUPr00N5bVbCDhMQ95wTo4Ptv/s0VT1ugVJUmoIGgtVQK3RjEBiH7nZg/E2Vo16zyTZtXglbeHm5KEup4YeEniQv0ga2OZn9JX9Cq6tPll3mlWCIkqoL33SQ++j+C7TDYWWEyQtJaoUFHsemVch2jjJepYstFz5FA2ZZIQADSI16rKYVet9kl2Itst/6Vcuk6GYjzUdAt3QSGFRIxHxRYfVXIbE+2dzBB83JcuLfq0pK0rShIQaCM6DsBUjGQ5ZuI9eGpP2IM1tBQ+/Uxxkt0/fGhmKsw1gDbvivFoWjauQM/2wmQ6ZEbiPvLEHt/DdHr8WI5avulB4oMhG88G2m6WdV+5n2W9uSsFsRBNuDMKM7gGAVOF0u3hacIklYxmA63D2QhpCE+5KcS6ervv+8EOEYXJA5w7XXfgAsrIMA8F5v8tLGpTECkVeYGDAR2cBKnP3m+3SX+77yfBgX41ImCQYYcltbWr0lEbSSxQAfg6U8UHiEIn3k1a4gBZWr2mE1kg=; _U=1zj1Y2CeHphfQ59w6ndZh7q5MCkL1DTv6HAfUxUIg-xSCtnxT3qmP8a8pYrkTBQnwIdsVfISUkDIpGKxoKmkdZ2gm0__9bB896jfIiE_gjgZjhGA4fDpaUn2mti90rCCAdqeJe_bmIBUNCpWy4BejEvwzbCPbAuRS4seMMGiOlykQFNi0b30DGw4lkXFghPySuALvfUvdFfvQtpFz2zT8ww; WLID=jLfLUpC9C0JOTleFPc1cVbHcEUK833rth2Nm3S47ibwoSWD4xlEXUK9iu+MfI2wI6K6Z2Ztrtlh5QB2x2zIJY2YHycUDJx2aDfZDM5LNFac=; ABDEF=V=13&ABDV=11&MRNB=1639282241480&MRB=0; imgv=lodlg=1; SUID=A; _EDGE_S=SID=24E3815EC7366FE82633904FC6186EB6; WLS=C=7c17b8fa1e6c1ada&N=%e9%91%ab%e8%bf%9c; _SS=SID=24E3815EC7366FE82633904FC6186EB6; SRCHUSR=DOB=20211019&T=1639805383000&TPC=1639805393000&POEX=W; ipv6=hit=1639808994830&t=4; _HPVN=CS=eyJQbiI6eyJDbiI6NTcsIlN0IjoyLCJRcyI6MCwiUHJvZCI6IlAifSwiU2MiOnsiQ24iOjU3LCJTdCI6MCwiUXMiOjAsIlByb2QiOiJIIn0sIlF6Ijp7IkNuIjo1NywiU3QiOjEsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMS0xMi0xOFQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6NTIxfQ==; SNRHOP=I=&TS=; SRCHHPGUSR=SRCHLANG=zh-Hans&BRW=NOTP&BRH=M&CW=686&CH=778&SW=1596&SH=998&DPR=1.7645833492279053&UTC=480&DM=0&HV=1639805465&BZA=0&WTS=63774486570'
    }

    response = requests.get(url, headers=headers,timeout=10)
    if response.status_code == 200:
        return response.text
    return None


def save_HTML(TitleName, html_text):
    # 把爬取下来的数据text化
    fileName = './/成品html文件夹/' + TitleName + '.html'
    # 持久化存储，
    with open(fileName, 'a', encoding='utf-8') as fp:  # 若文件不存在则创建，若存在则追加，这次会把十页内容放在一个HTML文档里面
        fp.write(html_text)


def lxml_search_(TitleName):
    fileName = './/成品html文件夹/' + TitleName + '.html'
    html = etree.parse(fileName, etree.HTMLParser(encoding='utf-8'))  # 这行可以找到html文件，准备读取元素
    div_list = html.xpath('//div[@id="b_content"]//ol[@id="b_results"]/li[@class="b_algo"]')  # 里面包含了所有标题以及简介
    print("----div_list,指向包含一切元素的‘b_algo’：")
    title_href = div_list[0].xpath('//div[@class="b_title"]/h2/a/@href')
    print("----title_href,指向所有标题的链接’：")
    print("title_href:", title_href)
    print("len(title_herf)", len(title_href))
    original_title_text = div_list[0].xpath('//div[@class="b_title"]/h2/a//text()')

    front = div_list[0].xpath('//div[@class="b_title"]/h2/a')
    print("front:", front)
    print("len(front)", len(front))

    title_text = []
    for i in front:
        every_title_text = i.xpath("string(.)")
        title_text.append(every_title_text)
    print("title_text:", title_text)
    print("len(title_text)", len(title_text))

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建一个新表，后面的那个=0的意思是不压缩
    sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)
    # 在表book里创建一个新sheet，后面的那个True用于确认同一个cell单元是否可以重设值（True表示可以修改值）
    col = ('序号', '标题名', '标题链接')
    # 自定义列名（元组类型）
    for i in range(0, 3):
        sheet.write(0, i, col[i])  # 写入第一行
    # 写入函数，三个参数分别代表，第几行，第几列，要存放的数据（col元组值）
    for i in range(0, 1000):
        try:
            sheet.write(i + 1, 0, i)  # 写入第一列
            sheet.write(i + 1, 1, title_text[i])
            sheet.write(i + 1, 2, title_href[i])
        except:
            print("列表遍历完毕,开始保存")
            break
    savepath = './/成品excel文件夹/' + TitleName + '.xls'
    book.save(savepath)
    print('sucess')

#-----------------主程序代码------------------------------

all_funds_name = read_by_excel()  # all_funds_name保存的是所有基金名称列表
print(all_funds_name)
# ----------下面这一行可以调整爬取基金数量------------------
for each_fund_name in all_funds_name[2000:]:  # each_fund_name保存的是一个基金名,控制爬取基金数量
    original_url = output_url(each_fund_name)  # original_url保存的是初步的url
    # ----------下面这一行可以调整爬取页数------------------
    #try
    AimPages = changepage(original_url, 15)  # AimPages 将搜索引擎搜索基金的每一页都保存为url
    #except:

    print("一到十页的搜索引擎url(十个爬取目标)", AimPages)
    print(len(AimPages))

    for aimpage in AimPages:  # 将这十个页的url划分为单页处理
        html_text = get_one_page(aimpage)  # html_text里面保存的是网页源代码
        save_HTML(each_fund_name, html_text)  #保存为html格式，15页整合为一个
        time.sleep(random.randint(0,2))#每爬取一下就要随机设置时间间隔，防止封ip
        print(each_fund_name + '.html保存成功！')
    lxml_search_(each_fund_name)  #保存为excel格式
