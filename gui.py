import os
import tkinter as tk
from tkinter import PhotoImage
import subprocess
import threading
import time
from multiprocessing import Process

status = -1
start_t = time.time()
timest = 0 #0->left 1->right
x0,y0,x1,y1 = 0,0,9,3
clicking = 0
tab = {"111111":"1","111011":"2","11011":"3","10111":"4","10011":"5","011111":"6","011011":"7","01011":"8","00111":"9","00011":"0","111110":"q","111010":"w","11010":"e","10110":"r","10010":"t","011110":"y","011010":"u","01010":"i","00110":"o","00010":"p","111101":"a","111001":"s","11001":"d","10101":"f","10001":"g","011101":"h","011001":"j","01001":"k","00101":"l","00001":";","111100":"z","111000":"x","11000":"c","10100":"v","10000":"b","011100":"n","011000":"m","01000":",","00100":".","00000":"?"}
res = ""

def split():
    global timest
    global x0,x1,y0,y1
    while(True):
        # print("Switch")
        if x0!=x1:
            midx = (x0+x1)//2
            if(timest):
                timest = 0
                xx = x1
                x1 = midx
                draw()
                x1 = xx
            else:
                timest = 1
                xx = x0
                x0 = midx+1
                draw()
                x0 = xx 
        elif y0!=y1:
            midy = (y0+y1)//2
            if(timest):
                timest = 0
                yy = y1
                y1 = midy
                draw()
                y1 = yy
            else:
                timest = 1
                yy = y0
                y0 = midy+1
                draw()
                y0 = yy
        time.sleep(2)
        while(clicking):
            time.sleep(0.01)

def click():
    global x0,y0,x1,y1,start_t,res
    res+=str(timest)
    if x0!=x1:
        midx = (x0+x1)//2
        if(timest):
            x1 = midx
        else:
            x0 = midx+1
    elif y0!=y1:
        midy = (y0+y1)//2
        if(timest):
            y1 = midy
        else:
            y0 = midy+1

def draw_circle():
    global status  # 使用 global 關鍵字來訪問外部的 status 變數
    canvas.delete("circle")  # 清除之前的圓點
    x = canvas.winfo_reqwidth() - 30  # 右上角 x 座標
    y = canvas.winfo_reqheight() - 30  # 右上角 y 座標

    if status == -1:
        canvas.create_oval(x, y, x + 20, y + 20, fill="red", outline="red", tags="circle")
    elif status == 1:
        canvas.create_oval(x, y, x + 20, y + 20, fill="green", outline="green", tags="circle")
    elif status == 2:
        canvas.create_oval(x, y, x + 20, y + 20, fill="gray", outline="gray", tags="circle")

def read_output():
    global status
    reset()
    while True:
        output_line = process.stdout.readline()
        if not output_line:
            # continue
            break
        if output_line == "PoorSignal\n":
            status = -1
        elif output_line == "GreatSignal\n":
            status = 1
        elif output_line == "Click!\n": 
            clicking = 1
            status = 2
            click()
            draw()
            status = 2
            if x0==x1 and y0==y1:
                print(res)
                try:
                    print(tab[res])
                except:
                    print("Error")
                reset()
            clicking = 0
        elif output_line == "Cd_ends\n" and status != -1 :
            status = 1

        print("標準輸出:", output_line, end="")
        label_1.config(text=output_line)
        label_1.update()
        draw_circle()
        

exe_path = "main.exe"
process = subprocess.Popen(exe_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

window = tk.Tk()
window.title('test')
window.geometry('1260x600')
window.configure(background='white')
# print("hello!")


# 上方的文字區域
text_area = tk.Text(window, height=10, width=60)
text_area.pack(side=tk.TOP)

main_canva = tk.Canvas(window, width=900, height=360)
main_canva.pack(side=tk.BOTTOM)


# 下方的圖片
image = PhotoImage(file="keyborad.png")
image_item = main_canva.create_image(450,200,image=image) # 圖片正中間 x = 450,y = 200

rectg = main_canva.create_rectangle(60, 100, 845, 300, outline="blue", width=4,tags="rectangle")
# 一格是 78.5 px (x) 50 px (y)

def reset():
    global res,x0,y0,x1,y1
    res = ""
    x0 = 0
    y0 = 0
    x1 = 9
    y1 = 3
def draw():
    global x0,y0,x1,y1
    main_canva.delete("rectangle")
    rectg = main_canva.create_rectangle(60+x0*78.5, 100+y0*50, 845-(9-x1)*78.5, 300-(3-y1)*50, outline="blue", width=4,tags="rectangle")


# main_canva.tag_raise(rectg)

frame_1 = tk.Frame(window)
frame_1.pack(side=tk.BOTTOM, anchor=tk.SE)

label_1 = tk.Label(frame_1, text='OUTPUT')
label_1.pack(side=tk.TOP)

canvas = tk.Canvas(frame_1, width=30, height=30)  # 創建一個小的 Canvas 來放置圓點
canvas.pack(side=tk.TOP)
draw_circle()  # 初始繪製圓點

frame_2 = tk.Frame(window)

def mainloop_with_catch():
    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()
    # 等待子進程完成
    process.wait()
    # 獲取子進程的退出碼
    exit_code = process.returncode
    print("退出碼:", exit_code)

# 創建一個全局變數來標識子進程是否已完成
process_completed = False

# 啟動子進程讀取輸出
t = threading.Thread(target=read_output)
t2 = threading.Thread(target=split)
t.start()
t2.start()

mainloop_with_catch()

# 等待子進程完成
while not process_completed:
    pass
