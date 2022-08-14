import requests
import json
import re
import os

"""
请允许我叙述一下需求:
首先, 我可以在到任意片段时感到不满, 于是点击某个按键后实现continue的操作:
其次, 我在听完后, 点击任意键, 即可进行"下一个"操作
每一次, 都会生成一个历史文件(.html), 会在历史记录<.dictionary>中呈现
-----历史记录中的另外一个.py文件会担任另外的责任:
---------tkinter界面读取.html文件, 展示为web, 并且读取它
"""

def test():
    while 1:
        '''数据初始化'''
        WantNext = input("要再看一篇吗?(输入0结束):")
        if WantNext == '0':
            break
        url = 'https://interface.meiriyiwen.com/article/random?dev=1'
        '''爬虫及json数据转换'''
        response = requests.get(url)
        # print(resource_code.encode('utf-8').decode('unicode_escape'))#难以想象, 我们居然不用转码
        js = response.json()#因为源代码是js格式的
        data = js.get("data")
        author = data.get("author")
        print("author:{0}".format(author))
        title = data.get("title")
        print("title:{0}".format(title))
        content = data.get("content")
        pattern = re.compile(r'<[^>]+>', re.S) #这样会去除正文中的html标签
        content = pattern.sub('\n\t', content)
        print("content:{0}".format(content))
        words = len(title + author + content)
        # 选取完毕,开始合成朗读
        text = """听众朋友们大家好,本篇文章题目为:《{title}》,作者: {author},
                  全文共{words}字,需要{time}分钟,
                  {content}
                  
                  
                  
                  朗读结束,感谢倾听
                  
                """ .format(title=title,author=author,words=words,
                            time=int(words/200),content=content)
        print(text)
        text_in_html=text.replace("\n","<br>")
        #确保文件夹存在
        Ensure_Folder_exist("小说历史记录")
        html_filename = os.getcwd()+"\\小说历史记录\\" + title + "-" + author + ".html"
        # 将处理好的文本, 保存为html
        Look_with_html(text=text_in_html,filename=html_filename)
        # 将处理好的文本, 用机器声读出来
        pyttsx3_debug(text=text, language=0, rate=200, volume=1.0, filename="当前随机文章.mp3")


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
    engine.say(text)
    # engine.save_to_file("王德发，爱你", "filename.mp3")
    engine.save_to_file(text, filename)
    engine.runAndWait()
    engine.stop()

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
'''代码运行区域'''
test()

