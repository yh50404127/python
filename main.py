from tkinter import *
import tkinter.simpledialog
import tkinter.messagebox
from init_firebase import *
import time
import threading


class BaseDesk:
    def __init__(self, master, db):
        self.root = master
        self.db = db

        self.root.config(bg="Silver")
        self.root.title('window')
        self.root.geometry('500x300')
        self.root.resizable(False, False)

        InitFace(self.root, self.db)


class InitFace:
    def __init__(self, master, db):

        self.db = db
        self.master = master
        self.master.geometry('500x300')
        self.f_login = Frame(self.master,bg="Silver", height=300, width=500)
        self.f_login.place(x=0, y=0)

        self.s1 = StringVar()
        self.s2 = StringVar()

        Label(self.f_login, text="帳號:", font='Helvetica 15', bg="Silver").place(x=85, y=60)
        Label(self.f_login, text="密碼:", font='Helvetica 15', bg="Silver").place(x=85, y=110)

        Entry(self.f_login, font='Helvetica 15', textvariable=self.s1).place(x=165, y=60)
        Entry(self.f_login, show="*", font='Helvetica 15', textvariable=self.s2).place(x=165, y=110)

        Button(self.f_login, text='登入', font='Helvetica 15', command=self.login).place(x=140, y=170)
        Button(self.f_login, text='註冊帳號', font='Helvetica 15', command=self.register).place(x=270, y=170)

        self.lab3 = Label(self.f_login,
                          text="",  # 成功Green 失敗Red
                          bg="Silver",
                          font='Helvetica 15')
        self.lab3.place(x=195, y=235)

    def change(self,):
        self.f_login.destroy()
        Face1(self.master, self.db, self.s1.get())

    def login(self):

        if not self.s1.get() or not self.s2.get():
            tkinter.messagebox.showerror(title='錯誤', message='帳號或密碼錯誤')
            return

        s = 'users/' + self.s1.get()

        user_dict = firebase_read(self.db, s)

        if not user_dict:
            tkinter.messagebox.showerror(title='錯誤', message='帳號或密碼錯誤')
            return

        if self.s1.get() == user_dict["user"] and self.s2.get() == user_dict["password"]:
            self.lab3["text"] = "登入成功"
            self.lab3["fg"] = "Green"
            self.change()
        else:
            tkinter.messagebox.showerror(title='錯誤', message='帳號或密碼錯誤')
            self.lab3["text"] = "登入失敗"
            self.lab3["fg"] = "Red"

    def register(self):

        user = tkinter.simpledialog.askstring(title='帳號註冊',
                                              prompt='請輸入要註冊的帳號：')

        password = tkinter.simpledialog.askstring(title='輸入密碼',
                                                  prompt='輸入你的密碼：')

        if not user or not password:
            tkinter.messagebox.showerror(title='錯誤', message='註冊錯誤')
            return

        s = "users/" + user
        user_dict = firebase_read(self.db, s)

        if user_dict:
            tkinter.messagebox.showerror(title='錯誤', message='此帳號已被註冊')
            return
        else:
            d = {
                "user": user,
                "password": password
            }
            firebase_add(self.db, s, d)
            tkinter.messagebox.showinfo(title='成功', message='註冊成功')


def d_msg(db):
    msgs_ref = db.collection("messages")
    msgs = msgs_ref.get()

    if len(msgs) > 100:
        msgs_list = []
        for msg in msgs[:50]:
            msgs_list.append(msg.id)
        for i in range(50):
            x = "messages/" + msgs_list[i]
            firebase_delete(db, x)


class Face1:
    def __init__(self, master, db, user_name):

        self.master = master
        self.db = db
        self.user_name = user_name

        self.master.config(bg='Silver')
        self.master.geometry('700x700')

        self.face1 = Frame(self.master, bg="Silver", height=700, width=700)
        self.face1.place(x=0, y=0)

        user_name_s = "帳號: " + user_name

        Label(self.face1, text=user_name_s, font='Helvetica 15', bg="Silver").place(x=10, y=15)

        f1 = Frame(self.face1)
        f1.place(x=10, y=60)
        self.text1 = Text(f1,
                          font='Helvetica 15',
                          height=18,
                          width=47,
                          state=DISABLED
                          )
        self.text1.pack(side=LEFT)
        self.scr = Scrollbar(f1)
        self.scr.pack(side=RIGHT, fill=Y)
        self.scr.config(command=self.text1.yview)
        self.text1.config(yscrollcommand=self.scr.set)

        f2 = Frame(self.face1)
        f2.place(x=10, y=590)
        self.text2 = Text(f2, height=3, width=39, font='Helvetica 15')
        self.text2.pack(side=LEFT)
        scr = Scrollbar(f2)
        scr.pack(side=RIGHT, fill=Y)
        scr.config(command=self.text2.yview)
        self.text2.config(yscrollcommand=scr.set)

        mes_list = []

        callback_done = threading.Event()

        def on_snapshot(doc_snapshot, changes, read_time):
            nonlocal mes_list, self

            for doc in doc_snapshot:
                mes_dict = doc.to_dict()
                m = mes_dict["user"] + " : " + "\n" + mes_dict["mes"] + "\n"
                self.text1.config(state=NORMAL)

                if doc.id not in mes_list:
                    self.text1.insert(END, m)

                self.text1.config(state=DISABLED)
                mes_list.append(doc.id)
            callback_done.set()

            self.text1.yview_moveto('1.0')

        doc_ref = self.db.collection('messages')

        doc_ref.on_snapshot(on_snapshot)

        Button(self.face1, text='傳送', font='Helvetica 15', command=self.mes_send).place(x=600, y=610)
        Button(self.face1, text='登出', font='Helvetica 12', command=self.back).place(x=610, y=15)

    def back(self):
        self.face1.destroy()
        InitFace(self.master, self.db)

    def mes_send(self):
        t = time.asctime()
        t = t.replace(" ", "_")
        s = self.text2.get("1.0", "end")
        if len(s) == 1:
            return
        d = {
            "user":self.user_name,
            "mes":s
        }
        pa = "messages/" + t
        firebase_add(self.db, pa, d)

        self.text2.delete("1.0", "end")

        thread_d_msg = threading.Thread(target=d_msg, args=[self.db])
        thread_d_msg.start()


root = Tk()
db_base = init_firebase()
BaseDesk(root, db_base)
root.mainloop()
