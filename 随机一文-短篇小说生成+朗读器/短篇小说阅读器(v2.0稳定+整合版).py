'''
经过作者一周的重度使用, 发现了软件设计的不合理之处(自动化/集成化程度低)
因此, 迎来1.2版本的重大更新
- 重新设计了UI界面
- 将刷新模块和预览模块的功能集成化, 自动化
'''
import tkinter as tk
import tkinter.filedialog as filedialog

def Refresh_novel():#"刷新"按钮的函数
    import requests
    import re
    import os
    #你可以这样理解, 我把刷新一个短篇小说的功能放在这个函数里面了
    url = 'https://interface.meiriyiwen.com/article/random?dev=1'
    '''爬虫及json数据转换'''
    response = requests.get(url)
    # print(resource_code.encode('utf-8').decode('unicode_escape'))#难以想象, 我们居然不用转码
    js = response.json()  # 因为源代码是js格式的
    data = js.get("data")
    author = data.get("author")
    print("author:{0}".format(author))
    title = data.get("title")
    print("title:{0}".format(title))
    content = data.get("content")
    pattern = re.compile(r'<[^>]+>', re.S)  # 这样会去除正文中的html标签
    content = pattern.sub('\n\t', content)
    print("content:{0}".format(content))
    words = len(title + author + content)
    # 选取完毕,开始合成朗读
    text = """听众朋友们大家好,本篇文章题目为:《{title}》,作者: {author},
                      全文共{words}字,需要{time}分钟,
                      {content}



                      朗读结束,感谢倾听

                    """.format(title=title, author=author, words=words,
                               time=int(words / 200), content=content)
    print(text)
    text_in_html = text.replace("\n", "<br>")
    # 确保文件夹存在
    Ensure_Folder_exist("小说历史记录")
    html_filename = os.getcwd() + "\\小说历史记录\\" + title + "-" + author + ".html"
    # 将处理好的文本, 保存为html
    Look_with_html(text=text_in_html, filename=html_filename)
    # 自动填入变量
    full_file_path.set(html_filename)#这里是选择的全路径
    html_filename = html_filename.replace('\\','/')
    part_of_path = str(html_filename).split('/')[-1]  # 这里处理，在entry中显示
    part_file_path.set(part_of_path)#这里是输入框显示的路径
    Speak_HTML()

def Look_with_html(text,filename):#将文字转成html, 并保存为html
    import webbrowser
    with open (filename,'w',encoding='utf-8') as fp:
        message = """
                <html>
                <head>
                    <script>
                        function light_function()
                            {
                                document.getElementById("text_content").style.color="black";
                                document.getElementById("text_content").style.backgroundColor="rgba(0,0,0,0.1)";
                                document.body.style.backgroundImage="url('https://www.helloimg.com/images/2022/08/05/Z0WHyo.png')";
                            }
                        function Dark_function()
                            {
                                document.getElementById("text_content").style.color="white";
                                document.getElementById("text_content").style.backgroundColor="rgba(255,255,255,0.2)";
                                document.body.style.backgroundImage="url('https://www.helloimg.com/images/2022/08/04/Z0l5qt.png')";
                            }
                    </script>
                    <style>
                        body  {background-image:url('https://www.helloimg.com/images/2022/08/04/Z0l5qt.png');}
                        .choice-button { /* 按钮美化 */
        	                            width: 60px; /* 宽度 */
        	                            height: 40px; /* 高度 */
        	                            border-width: 0px; /* 边框宽度 */
        	                            border-radius: 3px; /* 边框半径 */
        	                            background: #1E90FF; /* 背景颜色 */
        	                            cursor: pointer; /* 鼠标移入按钮范围时出现手势 */
        	                            outline: none; /* 不显示轮廓线 */
        	                            font-family: Microsoft YaHei; /* 设置字体 */
        	                            color: white; /* 字体颜色 */
        	                            font-size: 17px; /* 字体大小 */
                                      }
                        .choice-button:hover { /* 鼠标移入按钮范围时改变颜色 */
                            background: #5599FF;
                        }
                    </style>
                </head>
                <body>
                <div>
                    <button id="dark_btn" class="choice-button" style="position: absolute;right:1%;top:5%;background:#455ede" onclick="Dark_function()">☪</button>
                    <button id="light_btn" class="choice-button" style="position: absolute;right:7%;top:5%;background:#ff6d00" onclick="light_function()">☀</button>
                    <div id="text_content" style="position: absolute;left:20%;top:10%;width:60%;padding:10px;font-size:20px;color:white;background-color:rgba(255,255,255,0.2)">
                """ + text + """ 
                    </div>
                </div>
                </body>
                </html>"""
        fp.write(message)
    webbrowser.open_new_tab(filename)

def Ensure_Folder_exist(folderPath):
    import os
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
        print("判断图片保存文件夹不存在,但是没有关系!已经创建了新的")

def Select_file():#"选择"按钮的函数
    try:
        full_path = filedialog.askopenfilename(title="选择存储关键词的文件", initialdir=".小说历史记录")
    except:
        full_path = filedialog.askopenfilename(title="选择存储关键词的文件", initialdir=".")
    full_file_path.set(full_path)#这里是选择的全路径
    # part_of_path = str(full_path).split('/')[-2]+'/'+str(full_path).split('/')[-1]#这里处理，在entry中显示
    part_of_path = str(full_path).split('/')[-1] #我决定只显示小说名字(避免太长无法显示)
    part_file_path.set(part_of_path)

def Preview_HTML():#"预览"按钮的函数
    import webbrowser
    filename = str(full_file_path.get())#选取之前存放的html全路径
    webbrowser.open_new_tab(filename)#在浏览器中打开该文件

def Speak_HTML():
    from bs4 import BeautifulSoup
    filename = str(full_file_path.get())
    with open (filename,"r",encoding='utf-8') as fp:#将html源代码提取出来
        lines_list = fp.readlines()
        content = ""
        for temp in lines_list:
            content += temp
    # content = content.replace("<br>", "\n")
    # print(content)#html文本内容读取完毕
    soup = BeautifulSoup(str(content), 'html.parser')#初始化文字，使之变为HTML结构
    try:
        article = soup.select('#text_content')[0].text #选取正文所在的节点
    except:
        article = soup.select('div')[0].text  # 选取正文所在的节点
    print(article)#正文选取成功
    pyttsx3_debug(text=article, language=0, rate=200, volume=1.0, filename="听历史文章-缓存.mp3")#读出文字

def pyttsx3_debug(text,language,rate,volume,filename):#这是一个通用函数, 用来读出来文字
    #需求: 四个重要参数,阅读的文字,语言,语速,音量,保存的文件名
    import pyttsx3
    engine = pyttsx3.init()  # 初始化语音引擎
    engine.setProperty('rate', rate)  # 设置语速
    #速度调试结果:50戏剧化的慢,200正常,350用心听小说,500敷衍了事
    engine.setProperty('volume', volume)  # 设置音量
    voices = engine.getProperty('voices')  # 获取当前语音的详细信息
    if int(language)==0:
        engine.setProperty('voice', voices[0].id)  # 设置第一个语音合成器 #改变索引，改变声音。0中文,1英文(只有这两个选择)
    elif int(language)==1:
        engine.setProperty('voice', voices[1].id)
    # engine.say(text)
    # engine.save_to_file("王德发，爱你", "filename.mp3")
    engine.save_to_file(text, filename)#为了让tkinter不卡顿，这里只保存为mp3，而不阅读
    engine.runAndWait()#一定要这一行才能保存成功
    engine.stop()
    import os
    os.system(filename)#调用系统自带的播放器播放MP3

def Delete_file():
    import os
    del_filename = full_file_path.get()
    os.remove(del_filename)
    full_file_path.set('')
    part_file_path.set('文件已删除')

window = tk.Tk()
window.title("短篇小说阅读器(v1.2稳定版)")
window.configure(bg='#fcbad3')
full_file_path = tk.StringVar()
part_file_path = tk.StringVar()
Refresh_Btn = tk.Button(window, text="开个盲盒噻 ⟳", command=Refresh_novel, bg='#a8d8ea')
Refresh_Btn.grid(row=0, column=0, columnspan=3, sticky=tk.W + tk.E)
txt_file_entry = tk.Entry(window, width=30, textvariable=part_file_path, bg='#fcbad3', relief="flat")
txt_file_entry.grid(row=1, column=0, columnspan=2)
Select_Btn = tk.Button(window, text="选择 ➜", command=Select_file, bg='#aa96da')
Select_Btn.grid(row=1, column=2, sticky=tk.W + tk.E)
Preview_Btn = tk.Button(window, text="预览 👁", command=Preview_HTML, bg='#ffd460')
Preview_Btn.grid(row=2, column=0, sticky=tk.W + tk.E)
Speak_Btn = tk.Button(window, text="阅读 ♬", command=Speak_HTML, bg='#f07b3f')
Speak_Btn.grid(row=2, column=1, sticky=tk.W + tk.E)
Delete_Btn = tk.Button(window, text=" 删除 🗑", command=Delete_file, bg='#FF4F4F')
Delete_Btn.grid(row=2, column=2, sticky=tk.W + tk.E)
window.mainloop()
