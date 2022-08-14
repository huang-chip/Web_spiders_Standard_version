import tkinter as tk
import tkinter.filedialog as filedialog

def Select_file():#"选择"按钮的函数
    try:
        full_path = filedialog.askopenfilename(title="选择存储关键词的文件", initialdir=".小说历史记录")
    except:
        full_path = filedialog.askopenfilename(title="选择存储关键词的文件", initialdir=".")
    full_file_path.set(full_path)#这里是选择的全路径
    part_of_path = str(full_path).split('/')[-2]+'/'+str(full_path).split('/')[-1]#这里处理，在entry中显示
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

window = tk.Tk()
window.title("选取现有html并阅读")
full_file_path = tk.StringVar()
part_file_path = tk.StringVar()
txt_file_entry = tk.Entry(window, width=40, textvariable=part_file_path)
txt_file_entry.grid(row=0, column=0)
Select_Btn = tk.Button(window, text="选择", command=Select_file)
Select_Btn.grid(row=0, column=1)
Preview_Btn = tk.Button(window, text="预览", command=Preview_HTML)
Preview_Btn.grid(row=1, column=0)
Speak_Btn = tk.Button(window, text="阅读", command=Speak_HTML)
Speak_Btn.grid(row=1, column=1)
window.mainloop()
