try:
    from tkinter import *
    import tkinter
    import tkinter.messagebox
    #from tkinter import Tk
    #from tkinter import Canvas
    #from tkinter import messagebox
    import serial
    import os
    import time
    import threading
    import sys
    import math
except:
    pass

# 《能力值公式》

# 「不論轉生幾次，單一屬性能力不可能超過玩家轉生前等級的３倍」
# 「轉生後的屬性=10+能力值×〔（(轉生次數-1)×10）+(能力值÷2)+(等級÷2)〕÷1000」
# 「其中能力值÷２的數值上限是（250+(轉生次數-1)×10）」

# 假設某刀戰在等級８０時第１次轉生，而轉生時的力量是１６０，這位刀戰的轉生後的屬性就是10+160×〔(80÷2+160÷2)÷1000〕=29，所以轉生後的力量屬性就是29點。轉生前的等級是80，29小於80×3，所以屬性不變。


# 《生命與法力公式》

# 「轉生後的生命值或法力值不可超過〔2000+(已轉生次數-1)×500〕」
# 「轉生後的生命=100+生命值×〔（(轉生次數-1)×10）+(生命值÷1000)+(等級÷2)〕÷1000。
# 其中生命值÷1000的數值上限最多計算到50」（法力的公式也一模一樣）

# 假設，某光使在等級１８０時，去第１６次轉生，而轉生時的法力是40000，轉生後法力為100+40000×〔（(16-1)×10+(40000÷1000)+(180÷2)）〕÷1000=11300。由於11300已經大於〔2000+(16-1)×500〕，所以轉生後的法力值是9500。

# 2019.08.19
# 2. 起始轉生等級從71及改成101級。
# 3. 公式最後的÷1000改成÷1500


def getData():
    #----------------------------INPUT-------------------------------
    lv = int(enput[1].get()) #LV
    n = int(enput[2].get()) #number of turns
    fac = int(enput[3].get()) #factor:1000,1500
    HP = int(enput[4].get()) #before
    MP = int(enput[5].get()) #before
    #print(L,N,fac,HP,MP)
    for x in range(3,9):
        #s[3] = enput[6]  s[8]= enput[11]
        s[x] = (int(enput[x+3].get()))
        #print(s[x])
    #----------------------------BEFORE MAX-------------------------------
    #print(fac*(3*L-10))
    #print((20*(N-1)+math.ceil((L/2))+250))
    #print(smax)
    
    

    # sbmax = math.ceil(fac*(3*lv-10)/(20*(N-1)+math.ceil((lv/2))+250))
    # rd = math.floor(lv/2)+10*(N-1)
    # hbmax = math.ceil((-1*rd + math.ceil(math.sqrt(rd*rd+4*(1900+(N-1)*500))))*fac/2)
    # print(hbmax)
    #----------------------------AFTER MAX-------------------------------
    hp_on_1000_factor = math.floor((HP/fac)) if math.floor((HP/fac))<=50 else 50
    mp_on_1000_factor = math.floor((MP/fac)) if math.floor((MP/fac))<=50 else 50

    HPmax = 2000+(n-1)*500
    MPmax = HPmax
    Smax = 3 * lv
    
    # 「轉生後的屬性=10+能力值×〔（(轉生次數-1)×10）+(能力值÷2)+(等級÷2)〕÷1000」

    # 轉生前最大
    S_max_before = math.ceil((3*lv -10) *fac / (250+20*(n-1)+math.floor(lv/2)))
    for x in range(3,9):
        textout[x].config(text=str(S_max_before), background="#15a7ac" if s[x] <= S_max_before else "yellow", fg="#1e1e1e" if s[x] <= S_max_before else "red")

    # 轉生後最大
    for x in range(19,25):
        textout[x].config(text=str(Smax), background="#15a7ac" if s[x-19+3] <= S_max_before else "yellow", fg="#1e1e1e" if s[x-19+3] <= S_max_before else "red")

    # 轉生後
    b_on_2_factor = [0,0,0]
    S_after = [0,0,0]
    for x in range(3,9):
        b_on_2_factor.append(math.floor(s[x]/2) if (math.floor(s[x]/2) <= (250+10*(n-1))) else (250+10*(n-1)))
        S_after.append(math.floor(10+s[x]*((n-1)*10+b_on_2_factor[x]+math.floor(lv/2))/fac))
        textout[x+8].config(text=str(S_after[x]) if S_after[x]<=Smax else Smax, background="#15a7ac" if s[x] <= S_max_before else "yellow", fg="#1e1e1e" if s[x] <= S_max_before else "red")
  
    

    # 「轉生後的生命值或法力值不可超過〔2000+(已轉生次數-1)×500〕」
    # 「轉生後的生命=100+生命值×〔（(轉生次數-1)×10）+(生命值÷1000)+(等級÷2)〕÷1000。
    #  其中生命值÷1000的數值上限最多計算到50」（法力的公式也一模一樣）

    # 轉生後
    HP_after = math.floor(100 + HP*((n-1)*10+hp_on_1000_factor+math.floor(lv/2))/fac)
    MP_after = math.floor(100 + MP*((n-1)*10+mp_on_1000_factor+math.floor(lv/2))/fac)

    # 轉生後最大
    textout[17].config(text=str(HPmax), background="#15a7ac" if HP_after<=HPmax else "yellow", fg="#1e1e1e" if HP_after<=HPmax else "red")
    textout[18].config(text=str(MPmax), background="#15a7ac" if MP_after<=MPmax else "yellow", fg="#1e1e1e" if MP_after<=MPmax else "red")

    # 轉生後
    textout[9].config(text=str(HP_after) if HP_after<=HPmax else HPmax, background="#15a7ac" if HP_after<=HPmax else "yellow", fg="#1e1e1e" if HP_after<=HPmax else "red")
    textout[10].config(text=str(MP_after) if MP_after<=HPmax else MPmax, background="#15a7ac" if MP_after<=MPmax else "yellow", fg="#1e1e1e" if MP_after<=MPmax else "red")

    # 轉生前最大
    
    quad_b = fac*((n-1)*10 + math.floor(lv/2))
    quad_c = -1*fac*fac*(1900+(n-1)*50)
    #print(quad_c)
    print(quad_b)
    print(quad_c)
    HP_max_before = math.floor((-quad_b + math.sqrt(quad_b*quad_b-4*quad_c))/2)

    #HP_max_before = math.ceil(((2000+(n-1)*500) - 100)* fac /(10+10*(n-1)+math.floor(lv/2)))
    



    # rd = (n-1)*10 + math.floor(lv/2)
    # hbmax = math.ceil((-1*rd + math.ceil(math.sqrt(rd*rd-4*(1900+(n-1)*500))))*fac/2)
    #print(hbmax)

    MP_max_before = HP_max_before
    textout[1].config(text=str(HP_max_before) , background="#15a7ac" if HP_after<=HPmax else "yellow", fg="#1e1e1e" if HP_after<=HPmax else "red")
    #textout[2].config(text=str(hbmax) , background="#15a7ac" if MP_after<=MPmax else "yellow", fg="#1e1e1e" if MP_after<=MPmax else "red")



    # if (HP<=hbmax):
    #     textout[17].config(text=str(hamax), background="#15a7ac", fg="#1e1e1e")
    # else:
    #     textout[17].config(text=str(hamax), background="yellow", fg="red")
    # if (MP<=hbmax):
    #     textout[18].config(text=str(hamax), background="#15a7ac", fg="#1e1e1e")
    # else:
    #     textout[18].config(text=str(hamax), background="yellow", fg="red")
    # for x in range(19,25):
    #     if (s[x-19+3]<=sbmax):
    #         textout[x].config(text=str(samax), background="#15a7ac", fg="#1e1e1e")
    #     else:
    #         textout[x].config(text=str(samax), background="yellow", fg="red")
    # #----------------------------AFTER HMP -------------------------------
    # if (math.floor(HP/fac)<=50):
    #     if (math.floor(100+ HP*(10*(N-1)+math.floor(HP/fac)+math.floor(L/2))/fac)<=hamax):
    #         ha = math.floor(100+ HP*(10*(N-1)+math.floor(HP/fac)+math.floor(L/2))/fac)
    #     else:
    #         ha = hamax
    # else:
    #     if math.floor(100+ HP*(10*(N-1)+50+math.floor(L/2))/fac)<=hamax:
    #         ha = math.floor(100+ HP*(10*(N-1)+50+math.floor(L/2))/fac)
    #     else:
    #         ha = hamax
    # textout[9].config(text=str(ha), background="#15a7ac", fg="#1e1e1e")

    # if (math.floor(MP/fac)<=50):
    #     if (math.floor(100+ MP*(10*(N-1)+math.floor(MP/fac)+math.floor(L/2))/fac)<=hamax):
    #         ma = math.floor(100+ MP*(10*(N-1)+math.floor(MP/fac)+math.floor(L/2))/fac)
    #     else:
    #         ma = hamax
    # else:
    #     if math.floor(100+ MP*(10*(N-1)+50+math.floor(L/2))/fac)<=hamax:
    #         ma = math.floor(100+ MP*(10*(N-1)+50+math.floor(L/2))/fac)
    #     else:
    #         ma = hamax
    # textout[10].config(text=str(ma), background="#15a7ac", fg="#1e1e1e")
    # #----------------------------AFTER S  -------------------------------
    # sb=[]
    # for x in range(1,13):
    #     sb.append(0)
    # for x in range(3,9):
    #     if (s[x]/2<=250+10*(N-1)):
    #         if (math.floor(10+s[x]*((N-1)*10+math.floor(L/2)+math.floor(s[x]/2))/fac)<=L*3):
    #             sb[x]=math.floor(10+s[x]*((N-1)*10+math.floor(L/2)+(s[x]/2))/fac)
    #         else:
    #             sb[x]=L*3
    #     else:
    #         if (math.floor(10+s[x]*((N-1)*10+math.floor(L/2)+math.floor(250+10*(N-1)))/fac)<=L*3):
    #             sb[x]=math.floor(10+s[x]*((N-1)*10+math.floor(L/2)+(250+10*(N-1)))/fac)
    #         else:
    #             sb[x]=L*3

    #     if (s[x]<=sbmax):
    #         textout[x+8].config(text=str(sb[x]), background="#15a7ac", fg="#1e1e1e")
    #     else:
    #         textout[x+8].config(text=str(samax), background="yellow", fg="red")

def callback(event):
    print("clicked at", event.x, event.y)

global enput
enput = []
enput.append(0)
textout = []
textout.append(0)
s = []
s.append(0)
for x in range(1,12):
    s.append(0)

if (__name__=="__main__"):
    root = Tk()
    root.title("童話王國復甦 轉生計算器 by Simon")
    canvas = Canvas(root, bg="#1e1e1e", width=500, height=400, borderwidth=0, highlightthickness=0)
    canvas.pack() #pack all in canvas

    Label(canvas, text="轉生前",bg="#d1cc47").place(x = 50, y = 20, anchor = "nw", width = "100")
    Label(canvas, text="極限",bg="#d1cc47").place(x = 160, y = 20, anchor = "nw", width = "50")

    Label(canvas, text="等級").place(x = 50, y = 50, anchor = "nw", width = "30")
    Label(canvas, text="次數").place(x = 50, y = 80, anchor = "nw", width = "30")
    Label(canvas, text="系數").place(x = 50, y = 110, anchor = "nw", width = "30")

    Label(canvas, text="血量").place(x = 50, y = 140, anchor = "nw", width = "30")
    Label(canvas, text="法力").place(x = 50, y = 170, anchor = "nw", width = "30")

    Label(canvas, text="力量").place(x = 50, y = 200, anchor = "nw", width = "30")
    Label(canvas, text="智慧").place(x = 50, y = 230, anchor = "nw", width = "30")
    Label(canvas, text="體質").place(x = 50, y = 260, anchor = "nw", width = "30")
    Label(canvas, text="敏捷").place(x = 50, y = 290, anchor = "nw", width = "30")
    Label(canvas, text="魅力").place(x = 50, y = 320, anchor = "nw", width = "30")
    Label(canvas, text="幸運").place(x = 50, y = 350, anchor = "nw", width = "30")
    
    Label(canvas, text="轉生後", bg="#47d1af").place(x = 250, y = 20, anchor = "nw", width = "100")
    Label(canvas, text="極限", bg="#47d1af").place(x = 360, y = 20, anchor = "nw", width = "50")

    Label(canvas, text="血量").place(x = 250, y = 140, anchor = "nw", width = "30")
    Label(canvas, text="法力").place(x = 250, y = 170, anchor = "nw", width = "30")

    Label(canvas, text="力量").place(x = 250, y = 200, anchor = "nw", width = "30")
    Label(canvas, text="智慧").place(x = 250, y = 230, anchor = "nw", width = "30")
    Label(canvas, text="體質").place(x = 250, y = 260, anchor = "nw", width = "30")
    Label(canvas, text="敏捷").place(x = 250, y = 290, anchor = "nw", width = "30")
    Label(canvas, text="魅力").place(x = 250, y = 320, anchor = "nw", width = "30")
    Label(canvas, text="幸運").place(x = 250, y = 350, anchor = "nw", width = "30")

    #initial values
    for x in range(1,12):
        enput.append(0)
        enput[x]= Entry(canvas)
        enput[x].place(x = 100, y = 50+(x-1)*30, anchor = "nw", height = "20", width = "50")
        if (x==1):
            enput[x].insert(0, "101")
        if (x==2):
            enput[x].insert(0, "1")
        if (x==3):
            enput[x].insert(0, "1000")
        if (x==4) or (x==5):
            enput[x].insert(0, "2000")
        if (x>=6):
            enput[x].insert(0, "5")
    
    for x in range(1,25):
        if (x<=8):
            textout.append(0)
            textout[x] = Label(canvas, bg='#1e1e1e', width = 20, text = "")
            textout[x].place(x = 160, y = 140+(x-1)*30, anchor = "nw", height = "20", width = "50")
        if (x>8) and (x<=16):
            textout.append(0)
            textout[x] = Label(canvas, bg='#1e1e1e', width = 20, text = "")
            textout[x].place(x = 300, y = 140+(x-9)*30, anchor = "nw", height = "20", width = "50")
        if (x>16):
            textout.append(0)
            textout[x] = Label(canvas, bg='#1e1e1e', width = 20, text = "")
            textout[x].place(x = 360, y = 140+(x-17)*30, anchor = "nw", height = "20", width = "50")

    #L1 = Label(canvas, text="").place(x = 100, y = 230, anchor = "nw", width = "30")
    Button(canvas, text="轉生！",bg="#bf7937", command=getData).place(x = 250, y = 50, anchor = "nw", width="160", height="50")
    
    root.bind("<Button-3>", callback)
    root.mainloop()