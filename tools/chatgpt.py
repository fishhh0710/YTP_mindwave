import os
import tkinter as tk
from tkinter import PhotoImage
import subprocess
import threading
import time

status = -1
timest = 0 # 0->left 1->right
start_t = time.time()
x0,y0,x1,y1 = 0,0,9,3

def split():
    global x0,x1,y0,y1
    ti = (time.time()-start_t)//3
    if x0!=x1:
        midx = (x0+x1)//2
        if(ti%2==0):
            xx = x1
            x1 = midx
            draw()
            x1 = xx
        else:
            xx = x0
            x0 = midx+1
            draw()
            x0 = xx 
    elif y0!=y1:
        midy = (y0+y1)//2
        if(ti%2==0):
            yy = y1
            y1 = midy
            draw()
            y1 = yy
        else:
            yy = y0
            y0 = midy+1
            draw()
            y0 = yy

def click():
    global x0,y0,x1,y1,start_t
    ti = (time.time() - start_t)//3
    print("ti=",ti)
    if x0!=x1:
        midx = (x0+x1)//2
        if(ti%2==0):
            x1 = midx
        else:
            x0 = midx+1
    elif y0!=y1:
        midy = (y0+y1)//2
        if(ti%2==0):
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

def  read_output():
    global status
    reset()
    while True:
        split()
        output_line = process.stdout.readline()
        if not output_line:
            break
        if output_line == "PoorSignal\n":
            status = -1
        elif output_line == "GreatSignal\n":
            status = 1
        elif output_line == "Click!\n": 
            click()
            draw()
            status = 2
            if x0==x1 and y0==y1:
                print("FIND!!!\n")
                reset()
        elif output_line == "Cd_ends\n" and status != -1 :
            status = 1

        print("標準輸出:", output_line, end="")
        label_1.config(text=output_line)
        label_1.update()
        draw_circle()
        

exe_path = "fake.exe"
process = subprocess.Popen(exe_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

window = tk.Tk()
window.title('test')
window.geometry('1260x600')
window.configure(background='white')


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
    global x0,y0,x1,y1
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
t.start()
t2 = threading.Thread(target=split)
t2.start()
mainloop_with_catch()

# 等待子進程完成
while not process_completed:
    pass
