#请把目标csv放在此py程序同级路径下哦
#记得把目标csv改名为: pre-pixiv-data.csv
import csv
import pandas as pd
import re
import time
import os
import speech

def Ensure_Folder_exist(folderPath):
    import os
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
        print("判断图片保存文件夹不存在,但是没有关系!已经创建了新的")

def Save_an_picture(urlname,filepath):#输入图片下载链接和图片保存的地址,将图片保存到目标地址
    import requests
    import time
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        # 上面就是朴实无华的请求头啦,可以在网页中点F12,在network控制台中,详情中就有如下信息,自己复制咯
        'Cookie': '[{"domain": ".pixiv.net", "expiry": 1720266472, "httpOnly": false, "name": "_ga", "path": "/", "secure": false, "value": "GA1.2.1152601155.1657194446"}, {"domain": ".pixiv.net", "expiry": 1720266472, "httpOnly": false, "name": "_ga_75BBYNYN9J", "path": "/", "secure": false, "value": "GS1.1.1657194446.1.1.1657194472.0"}, {"domain": "www.pixiv.net", "expiry": 1657799269, "httpOnly": false, "name": "QSI_S_ZN_5hF4My7Ad6VNNAi", "path": "/", "secure": false, "value": "v:0:0"}, {"domain": ".pixiv.net", "expiry": 1657196268, "httpOnly": false, "name": "__utmb", "path": "/", "secure": false, "value": "235335808.2.10.1657194445"}, {"domain": ".pixiv.net", "httpOnly": false, "name": "__utmc", "path": "/", "secure": false, "value": "235335808"}, {"domain": ".pixiv.net", "expiry": 1720266468, "httpOnly": false, "name": "__utmv", "path": "/", "secure": false, "value": "235335808.|3=plan=normal=1^5=gender=male=1^6=user_id=82595799=1^11=lang=zh=1"}, {"domain": ".pixiv.net", "expiry": 1720266468, "httpOnly": false, "name": "c_type", "path": "/", "secure": true, "value": "19"}, {"domain": ".pixiv.net", "expiry": 1720266468, "httpOnly": false, "name": "b_type", "path": "/", "secure": true, "value": "1"}, {"domain": ".pixiv.net", "expiry": 1720266468, "httpOnly": false, "name": "a_type", "path": "/", "secure": true, "value": "0"}, {"domain": ".pixiv.net", "expiry": 1659786467, "httpOnly": true, "name": "device_token", "path": "/", "secure": true, "value": "230be0796b5289569217dc81329129dc"}, {"domain": ".pixiv.net", "expiry": 1659786468, "httpOnly": true, "name": "PHPSESSID", "path": "/", "secure": true, "value": "82595799_IP0bIaKDaZGbPkxeUsssBBWoHaKXrwbk"}, {"domain": ".pixiv.net", "expiry": 1657194509, "httpOnly": false, "name": "_gat_UA-1830249-3", "path": "/", "secure": false, "value": "1"}, {"domain": ".pixiv.net", "expiry": 1720266468, "httpOnly": true, "name": "privacy_policy_notification", "path": "/", "secure": true, "value": "0"}, {"domain": ".pixiv.net", "expiry": 1657280872, "httpOnly": false, "name": "_gid", "path": "/", "secure": false, "value": "GA1.2.1685291917.1657194450"}, {"domain": ".pixiv.net", "expiry": 1720266467, "httpOnly": true, "name": "privacy_policy_agreement", "path": "/", "secure": true, "value": "3"}, {"domain": "www.pixiv.net", "expiry": 1720266444, "httpOnly": false, "name": "first_visit_datetime_pc", "path": "/", "secure": true, "value": "2022-07-07+20%3A47%3A25"}, {"domain": ".pixiv.net", "expiry": 1720266468, "httpOnly": false, "name": "__utma", "path": "/", "secure": false, "value": "235335808.1448897202.1657194445.1657194445.1657194445.1"}, {"domain": "www.pixiv.net", "expiry": 1720266444, "httpOnly": false, "name": "yuid_b", "path": "/", "secure": true, "value": "M0VgaEY"}, {"domain": ".pixiv.net", "expiry": 1672962468, "httpOnly": false, "name": "__utmz", "path": "/", "secure": false, "value": "235335808.1657194445.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"}, {"domain": ".pixiv.net", "expiry": 1720266468, "httpOnly": false, "name": "tag_view_ranking", "path": "/", "secure": true, "value": "mFosrNEiIG~FrSumU5wXT~QBodg0XINN~PUu9jDANP3~0Chn6pjoxR"}, {"domain": ".pixiv.net", "expiry": 1657195047, "httpOnly": false, "name": "__utmt", "path": "/", "secure": false, "value": "1"}, {"domain": ".pixiv.net", "expiry": 1814874444, "httpOnly": false, "name": "p_ab_id", "path": "/", "secure": true, "value": "7"}, {"domain": ".pixiv.net", "expiry": 1814874444, "httpOnly": false, "name": "p_ab_id_2", "path": "/", "secure": true, "value": "1"}, {"domain": ".pixiv.net", "expiry": 1657196246, "httpOnly": true, "name": "__cf_bm", "path": "/", "sameSite": "None", "secure": true, "value": "H2EuZK2z1IKhPAInokdn8abXuPQT7MWUwsv8VuGJcUE-1657194447-0-AUTEo1XEHr9/OQvET75amkskJ7TqP5/E9LExZwCy3WSCNNHjBlCrpMC9ce2//FQG2FthNnm5LYkVnc2ZV4IFUYf7xfT8angG8SnEiekVpFzuQfSj9f1WjtN+vJ84j/DTcv5WixTsT3/Wmn2o0VaxzyJLJtjQJSykY2DxYLkdk3sfI+7u3XjzCitrBvAy8dN7bsz0dByJOHj9FGM6F1nfyGs="}, {"domain": ".pixiv.net", "expiry": 1664970469, "httpOnly": false, "name": "_fbp", "path": "/", "sameSite": "Lax", "secure": false, "value": "fb.1.1657194446668.2118552828"}, {"domain": ".pixiv.net", "expiry": 1814874444, "httpOnly": false, "name": "p_ab_d_id", "path": "/", "secure": true, "value": "1182565364"}, {"domain": ".pixiv.net", "expiry": 1657194511, "httpOnly": false, "name": "_gat", "path": "/", "secure": false, "value": "1"}]',
        #Cookie中记录了自己的登录信息,有了正确的Cookie,网站才会识别出'我是某个用户'
        'referer': 'https://www.pixiv.net',
        #上面这条很重要,referer是告诉pixiv网站你是从pixiv.net点击进入图片详情页的,这样才不会报错403
        "Connection": "close"
        #上面这条可以跳过网站对SSL证书的检验
    }
    r = requests.get(urlname,headers=headers)#requests.get()是爬虫的基本基本方法,自己掌握哦
    img = r.content #对一个response对象,返回网页的源代码
    with open(filepath, 'wb') as f:
        #用二进制方式写入图片啦,with open()方法就是open()...f.close()的简化版本,我下期细说
        f.write(img)
    time.sleep(2)
    #time.sleep()方法,需要提前导入time库,程序在运行到这行代码时会休息x秒,这样减少网页负担,也防止被封ip

def Run_and_Download():
    # header是列名，是每一列的名字，如果header=1，将会以第二行作为列名，读取第二行以下的数据。
    csv_filename = csv_file_path.get()
    data = pd.read_csv(csv_filename,sep=',',header='infer')
    array=data.values[0::,0::]  #读取全部行，全部列
    # print(array)              #array是数组形式存储，顺序与data读取的数据顺序格式相同
    Ensure_Folder_exist('save_here')#文件夹不存在就创建一个~
    for i in range(len(array)):#array是一个二维数组,其中的每一个元素都是该行的内容
        temp = array[i]#temp代表第i行的所有内容,其中有下载链接和保存地址
        print("图片下载链接: ",temp[0])
        print("图片保存地址: ",temp[1])
        temp[1] = str(re.sub('[\:*?"<>|]', '_', temp[1]))
        if os.path.exists(temp[1]): #用os库监测图片保存地址是否存在,存在的话就无需再下载一次了
            print(temp[1],"已经存在,下一个!")
            i += 1
            # 下面是对进度条的操作
            if i % 10 != 0:
                progressbarTwo['value'] += 1
                print("progressbarTwo['value']", progressbarTwo['value'])
                window.update()
            elif i % 10 == 0:
                # progressbarTwo['value'] += 1
                progressbarTwo['value'] = 0
                progressbarOne['value'] += 10
                print("progressbarTwo['value']", progressbarTwo['value'])
                window.update()
            continue
        try:
            Save_an_picture(temp[0], temp[1])
        except:
            speech.say("出现错误")
            time.sleep(5)
            Save_an_picture(temp[0], temp[1])
        print('第{0}/{1}张图片下载完毕'.format(i+1,len(array)),end='\t\t')
        print("时间: ", time.strftime('%H:%M:%S', time.localtime(time.time())))  # 记录一下时间
        #下面是对进度条的操作
        if i%10 != 0:
            progressbarTwo['value'] += 1
            print("progressbarTwo['value']",progressbarTwo['value'])
            window.update()
        elif i%10 == 0:
            # progressbarTwo['value'] += 1
            progressbarTwo['value'] = 0
            progressbarOne['value'] += 10
            window.update()

#以下为tkinter页面的开发
def select_keyword_file():  # 这里绑定"选择"按钮
    csv_name = filedialog.askopenfilename(title="选择存储数据的.csv文件", initialdir=".", filetypes=(("CSV", ".csv"),))
    csv_file_path.set(csv_name)
    part_file_path.set(csv_name.split('/')[-2]+'/'+csv_name.split('/')[-1])

import tkinter as tk
import tkinter.ttk
import tkinter.filedialog as filedialog
window = tk.Tk()
window.title("解码csv并下载今日份插画~")
window.configure(bg='slategray')
csv_file_path = tk.StringVar()
part_file_path = tk.StringVar()

from tkinter import ttk
s = ttk.Style()
s.theme_use('classic')
# win10环境下,进度条样式主题：('winnative','clam','alt','default','classic','vista','xpnative')
# 进度条颜色改变测试成功的是：'winnative','clam','alt','default','classic'
# 转载自"http://wb98.com/post/340.html",非常全面的进度条讲解
s.configure("my0_GunDam.Horizontal.TProgressbar", troughcolor='#1f5fa0', background='#c00000')#这个实际上是定义了一个样式, 可以定义多条进度条样式, 使用时引用
s.configure("my1_Eva.Horizontal.TProgressbar", troughcolor='indigo', background='forestgreen')#这个实际上是定义了一个样式, 可以定义多条进度条样式, 使用时引用


lbl_file = tk.Label(window, text='选取csv文件:', fg='orange', bg='slategray', font=('黑体',12))
lbl_file.grid(row=0, column=0)

txt_file = tk.Entry(window, width=40, textvariable=part_file_path, bg='#df3035')
txt_file.grid(row=0, column=1, sticky=tk.W)

btn_file = tk.Button(window, text="选择", command=select_keyword_file, fg='gold', bg='#26292a')
btn_file.grid(row=0, column=3, sticky=tk.E+tk.W)

lbl_loading_keywords = tk.Label(window, text='下载进度:', fg='white', bg='slategray', font=('黑体',12))
lbl_loading_keywords.grid(row=1, column=0)

progressbarOne = tkinter.ttk.Progressbar(window, style="my0_GunDam.Horizontal.TProgressbar", maximum=500)
progressbarOne.grid(row=1, column=1, columnspan=1, sticky=tk.E+tk.W)

btn_begin = tk.Button(window, text="开始爬取", command=Run_and_Download, fg='gold', bg='dimgray')
btn_begin.grid(row=1, column=3, sticky=tk.E+tk.W)

progressbarTwo = tkinter.ttk.Progressbar(window, style="my1_Eva.Horizontal.TProgressbar", maximum=10)
progressbarTwo.grid(row=2, column=0, columnspan=4, sticky=tk.E+tk.W)

window.mainloop()
