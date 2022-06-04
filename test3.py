import threading
import tkinter as tk
from init_firebase import *


def change():
    global f1, window
    f1.destroy()
    window.title('xxx')
    window.geometry('700x500')
    window.config(bg="Red")
    window.resizable(False, False)
    f2 = tk.Frame(window)
    f2.pack()


window = tk.Tk()
window.title('window')
window.geometry('500x300')
window.config(bg="Silver")
window.resizable(False, False)

f1 = tk.Frame(window)
f1.pack()

btn = tk.Button(f1,text='change',command=change)
btn.pack()

db = init_firebase()

callback_done = threading.Event()


def on_snapshot(doc_snapshot, changes, read_time):

    for doc in doc_snapshot:
        print(doc.to_dict())
    callback_done.set()


doc_ref = db.collection('messages')

doc_watch = doc_ref.on_snapshot(on_snapshot)

window.mainloop()
