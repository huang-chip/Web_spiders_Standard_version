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

class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("BING_spider_UI")
        self.keyword_file_path = tk.StringVar()
        self.keywords_list = tk.StringVar()

        self.frame = tk.Frame(self)
        self.frame.pack(padx=10,pady=10)

        self.lbl_file = tk.Label(self.frame, text='选取关键词文件(.xls或.txt) : ')
        self.lbl_file.grid(row=0, column=0)

        self.txt_file = tk.Entry(self.frame, width=80, textvariable=self.keyword_file_path)
        self.txt_file.grid(row=0, column=1, sticky=tk.W)

        self.btn_file = tk.Button(self.frame, text="选择", command=self.select_keyword_file)
        self.btn_file.grid(row=0, column=2, sticky=tk.E)

        self.lbl_file = tk.Label(self.frame, text='请确认关键词:')
        self.lbl_file.grid(row=1, column=0)

        self.keyword_text = tk.Text(self.frame, height=4)
        # self.keyword_text.insert("end", self.keywords_list.get())#这个不可行的原因是初始化时, 可变变量为空
        self.keyword_text.grid(row=1, column=1,sticky=tk.W+tk.E)

        self.btn_start = tk.Button(self.frame, text="开始爬取" ,command=self.Set_many_url_From_KeywordsList)
        self.btn_start.grid(row=1, column=2, sticky=tk.E)

    def select_keyword_file(self):
        self.keyword_file_path.set(filedialog.askopenfilename(title="选择存储关键词的文件", initialdir="."))
        self.read_keyword_return_list()

    def read_keyword_return_list(self):
        keyword_file_name = self.keyword_file_path.get()
        if keyword_file_name.split('.')[-1]=='txt':
            print("文件类型读取成功,开始读取文件")
            keywords_list = []
            keywords_in_var = []
            with open(keyword_file_name,'r',encoding='utf-8') as fp:
                txt_content = fp.readlines()#将每一行保存为一个列表元素
                for line in txt_content:
                    each_keyword = line.replace("\n","")
                    keywords_in_var.append(each_keyword)#可变变量只放关键词
                    url = "https://cn.bing.com/search?q=" + each_keyword
                    keywords_list.append(url)#真正的url都放在return的列表中
            print(keywords_list,"\n",len(keywords_list))
            self.keywords_list.set(keywords_in_var)
            self.keyword_text.insert("end", self.keywords_list.get())
            return keywords_list
        else :
            print('文件名错了,请选择.txt格式的文件')

    def Set_many_url_From_KeywordsList(self):
        import requests
        from lxml import etree
        Keywords_List = self.read_keyword_return_list()
        for temp0 in Keywords_List:
            print(temp0)
            # 说一下思路, 首先获取源代码,取标题,链接,简介,存在结构体中,
            # 然后,找到"title=下一页",用正则提取出其中的"&first=101",经过比对加到下一组url中,如果和集合中一模一样,则选取元素后跳出循环

    def get_one_page(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Cookie': '_EDGE_V=1; MUID=23E68497FBCA6D5336429442FA186C48; MUIDB=23E68497FBCA6D5336429442FA186C48; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=1110198E704D49E6BB43FAD45FD394A2&dmnchg=1; MUIDV=NU=1; ANON=A=EA01BF5C569E5109ADB08E63FFFFFFFF&E=1a2e&W=1; NAP=V=1.9&E=19d4&C=n-o83IrB4U07LopXmvLrFaCUA2QwkLaXf_hs9TICIM4D1ZJtI8tPJQ&W=1; PPLState=1; _ITAB=STAB=TR; _tarLang=default=zh-Hans; _TTSS_OUT=hist=WyJlbiIsInpoLUhhbnMiXQ==; _TTSS_IN=hist=WyJlbiIsInpoLUhhbnMiLCJhdXRvLWRldGVjdCJd; KievRPSSecAuth=FABSBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACGnV4HNRGLRHEAQCnY5RD3dyn9vsQhRwH/XLVt3Err7wzhuIqxa/vBJ1e/7MUEmlNOdFwW1GKazHt1t7FIUEUW7SQ/4UoV+CiLMF8MQR5VcAsHZjeG8D8picQb2FMOhNPxdLhsL29a00Vugq7jivk6XXr2s1jQ04zmJAkIAWHzh4GPRSlBwE/ZecZ5AmyLqAL8p8YZ9MyRiK9CfmqC8TWnxeoKLlXBzVdp3Kntt8OyMTSiXvKXTFo/kw9zri4Rr53taB7o+bG44lGDKIdt9k4buQtClFxXH9BFsK9hF2rqd9gYAb42JI3aX3NCkVIRCZYtqoxqz7ZJX36n/rkASNXZacwxjbF6drrxstgk6EaTVFUec91U+jH/eNKi9WbT8iAy63pjUiDRb9dJzgjVWz8pVcbWitDAb3X8vBZ9cMn50m4bk8Ic6RRJ+sg2USyVt+sHZMTXOitl1rybqgEHsm5plQX1q3XXLuWlpdnwqEQMAT7EfFt4wu9qOB4XizmPPqbXrdZuqRjYT2jLvne79YnhbtDZKUzrRyH+yfrhH8gHFpqXRVjQuJWxqSkrHx1TBoO9Uztq6Or8YW7Vl4X2exKc3JWhPgKV5JN7XS3agMQvlbQvxtGjAke6FZwftnSlzTwDhDosbYNc1ZYCuE3r2970cLjgfZJ3SFTkGdJAqPVVXBX9JQkiPMd5vKo8UstmXs2pW9yEKfjaHU8SNnlG9iW6ocHr06gdTD407mSwDHyqTZf4WYct6K3JU6rEO2U+32QgA6Q2jGtbAhyFoRR6xrN+pkqXKGp9qG8FNbhAN/0PJLo4MUmdMhlCDarUMeFbEQuFshj3c6PNwhP5xuz+CvjBhRRDZJLyOkIBkFYr/4PMFk6XnClHg2uOuBpsz3yDcFXkcCsZoQQv174CjViZkLFIUPr00N5bVbCDhMQ95wTo4Ptv/s0VT1ugVJUmoIGgtVQK3RjEBiH7nZg/E2Vo16zyTZtXglbeHm5KEup4YeEniQv0ga2OZn9JX9Cq6tPll3mlWCIkqoL33SQ++j+C7TDYWWEyQtJaoUFHsemVch2jjJepYstFz5FA2ZZIQADSI16rKYVet9kl2Itst/6Vcuk6GYjzUdAt3QSGFRIxHxRYfVXIbE+2dzBB83JcuLfq0pK0rShIQaCM6DsBUjGQ5ZuI9eGpP2IM1tBQ+/Uxxkt0/fGhmKsw1gDbvivFoWjauQM/2wmQ6ZEbiPvLEHt/DdHr8WI5avulB4oMhG88G2m6WdV+5n2W9uSsFsRBNuDMKM7gGAVOF0u3hacIklYxmA63D2QhpCE+5KcS6ervv+8EOEYXJA5w7XXfgAsrIMA8F5v8tLGpTECkVeYGDAR2cBKnP3m+3SX+77yfBgX41ImCQYYcltbWr0lEbSSxQAfg6U8UHiEIn3k1a4gBZWr2mE1kg=; _U=1zj1Y2CeHphfQ59w6ndZh7q5MCkL1DTv6HAfUxUIg-xSCtnxT3qmP8a8pYrkTBQnwIdsVfISUkDIpGKxoKmkdZ2gm0__9bB896jfIiE_gjgZjhGA4fDpaUn2mti90rCCAdqeJe_bmIBUNCpWy4BejEvwzbCPbAuRS4seMMGiOlykQFNi0b30DGw4lkXFghPySuALvfUvdFfvQtpFz2zT8ww; WLID=jLfLUpC9C0JOTleFPc1cVbHcEUK833rth2Nm3S47ibwoSWD4xlEXUK9iu+MfI2wI6K6Z2Ztrtlh5QB2x2zIJY2YHycUDJx2aDfZDM5LNFac=; ABDEF=V=13&ABDV=11&MRNB=1639282241480&MRB=0; imgv=lodlg=1; SUID=A; _EDGE_S=SID=24E3815EC7366FE82633904FC6186EB6; WLS=C=7c17b8fa1e6c1ada&N=%e9%91%ab%e8%bf%9c; _SS=SID=24E3815EC7366FE82633904FC6186EB6; SRCHUSR=DOB=20211019&T=1639805383000&TPC=1639805393000&POEX=W; ipv6=hit=1639808994830&t=4; _HPVN=CS=eyJQbiI6eyJDbiI6NTcsIlN0IjoyLCJRcyI6MCwiUHJvZCI6IlAifSwiU2MiOnsiQ24iOjU3LCJTdCI6MCwiUXMiOjAsIlByb2QiOiJIIn0sIlF6Ijp7IkNuIjo1NywiU3QiOjEsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMS0xMi0xOFQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6NTIxfQ==; SNRHOP=I=&TS=; SRCHHPGUSR=SRCHLANG=zh-Hans&BRW=NOTP&BRH=M&CW=686&CH=778&SW=1596&SH=998&DPR=1.7645833492279053&UTC=480&DM=0&HV=1639805465&BZA=0&WTS=63774486570'
        }

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        return None

'''
        self.lbl_file = tk.Label(self.frame,text='图像')
        self.lbl_file.grid(row=0, column=0)

        self.txt_file = tk.Entry(self.frame, width=50, textvariable=self.img_path)
        self.txt_file.grid(row=0, column=1, sticky=tk.W)

        self.btn_file = tk.Button(self.frame, text="获取剪切板图片", command=self.copy_clipboard)
        self.btn_file.grid(row=0, column=1, sticky=tk.E)  # E表示靠左对齐,W向右对齐

        self.btn_file = tk.Button(self.frame, text="选择", command=self.sel_img_file)
        self.btn_file.grid(row=0, column=2, sticky=tk.E)

        self.show_img = tk.Label(self.frame)
        self.show_img.grid(row=1, column=1)


        self.lbl_txt = tk.Label(self.frame, text="文本")
        self.lbl_txt.grid(row=2, column=0)

        self.txt_extract = tk.Text(self.frame)
        self.txt_extract.grid(row=2, column=1)

        self.btn_extract = tk.Button(self.frame, text="提取文本", command=self.extract_text)
        self.btn_extract.grid(row=3, column=1, sticky=tk.W + tk.E)
'''



if __name__ == "__main__":
    import tkinter as tk
    import tkinter.filedialog as filedialog
    app = Application()
    app.mainloop()
