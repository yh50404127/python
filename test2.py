from tkinter import *
from init_firebase import *
import threading


def send():
    print("send")


def out():
    print("out")


db = init_firebase()
window = Tk()
window.title('window')
window.geometry('700x700')
window.config(bg="Silver")
window.resizable(False, False)

lab1 = Label(window, text="帳號:", font='Helvetica 15', bg="Silver").place(x=10, y=15)

f1 = Frame(window)
f1.place(x=10, y=60)

text1 = Text(f1,
             font='Helvetica 15',
             height=18,
             width=47,
             state=DISABLED
             )
text1.pack(side=LEFT)
scr = Scrollbar(f1)
scr.pack(side=RIGHT, fill=Y)
scr.config(command=text1.yview)
text1.config(yscrollcommand=scr.set)

f2 = Frame(window)
f2.place(x=10, y=590)
text2 = Text(f2, height=3, width=39, font='Helvetica 15')
text2.pack(side=LEFT)
scr = Scrollbar(f2)
scr.pack(side=RIGHT, fill=Y)
scr.config(command=text2.yview)
text2.config(yscrollcommand=scr.set)

btn1 = Button(window, text='傳送', font='Helvetica 15', command=send).place(x=600, y=610)
btn2 = Button(window, text="登出", font='Helvetica 12', command=out).place(x=610, y=15)

callback_done = threading.Event()


def on_snapshot(doc_snapshot, changes, read_time):

    for doc in doc_snapshot:
        mes_dict = doc.to_dict()
        m = mes_dict["user"] + " : " + mes_dict["mes"] + "\n"
        text1.config(state=NORMAL)
        text1.insert(END, m)
        text1.config(state=DISABLED)
    callback_done.set()


doc_ref = db.collection('messages')

doc_watch = doc_ref.on_snapshot(on_snapshot)


window.mainloop()

