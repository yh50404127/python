from tkinter import *
import tkinter.simpledialog
import tkinter.messagebox
from init_firebase import *


def login():

    global db, lab3

    if not s1.get() or not s2.get():
        tkinter.messagebox.showerror(title='錯誤', message='帳號或密碼錯誤')
        return

    s = 'users/' + s1.get()

    user_dict = firebase_read(db, s)

    if not user_dict:
        tkinter.messagebox.showerror(title='錯誤', message='帳號或密碼錯誤')
        return

    if s1.get() == user_dict["user"] and s2.get() == user_dict["password"]:
        lab3["text"] = "登入成功"
        lab3["fg"] = "Green"
    else:
        tkinter.messagebox.showerror(title='錯誤', message='帳號或密碼錯誤')
        lab3["text"] = "登入失敗"
        lab3["fg"] = "Red"


def register():

    global db

    user = tkinter.simpledialog.askstring(title='帳號註冊',
                                          prompt='請輸入要註冊的帳號：')

    password = tkinter.simpledialog.askstring(title='輸入密碼',
                                              prompt='輸入你的密碼：')

    if not user or not password:
        tkinter.messagebox.showerror(title='錯誤', message='註冊錯誤')
        return

    s = "users/" + user
    user_dict = firebase_read(db, s)

    if user_dict:
        tkinter.messagebox.showerror(title='錯誤', message='此帳號已被註冊')
        return
    else:
        d = {
            "user":user,
            "password":password
        }
        firebase_add(db, s, d)
        tkinter.messagebox.showinfo(title='成功', message='註冊成功')


db = init_firebase()
window = Tk()
window.title('window')
window.geometry('500x300')
window.config(bg="Silver")
window.resizable(False, False)

s1 = StringVar()
s2 = StringVar()

f_login = Frame(window).pack()

lab1 = Label(f_login, text="帳號:", font='Helvetica 15', bg="Silver").place(x=85, y=60)
lab2 = Label(f_login, text="密碼:", font='Helvetica 15', bg="Silver").place(x=85, y=110)

ent1 = Entry(f_login, font='Helvetica 15', textvariable=s1).place(x=165, y=60)
ent2 = Entry(f_login, show="*", font='Helvetica 15', textvariable=s2).place(x=165, y=110)

btn1 = Button(f_login, text='登入', font='Helvetica 15', command=login).place(x=140, y=170)
btn2 = Button(f_login, text='註冊帳號', font='Helvetica 15', command=register).place(x=270, y=170)

lab3 = Label(f_login,
             text="",  # 成功Green 失敗Red
             bg="Silver",
             font='Helvetica 15')
lab3.place(x=195, y=235)


window.mainloop()

