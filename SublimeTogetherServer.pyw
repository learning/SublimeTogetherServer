import os
import tkinter as tk
import tkinter.scrolledtext
import sqlite3
import time

DB = "./config.db"
conn = None

def is_database_exists():
    '''Check if database exists'''
    global DB
    return os.path.isfile(DB)

def connect_database():
    '''Connect to SQLite database'''
    global DB, conn
    inited = is_database_exists()
    conn = sqlite3.connect(DB)
    if not inited:
        init_database()

def init_database():
    '''Initialize database structrues'''
    execute_sql("CREATE TABLE users(username text, password text)")
    execute_sql("CREATE TABLE config(field text, content text)")
    execute_sql("INSERT INTO config VALUES('host', '0.0.0.0')")
    execute_sql("INSERT INTO config VALUES('port', '5800')")

def execute_sql(sql):
    '''Execute a sql clause'''
    global conn
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    c.close()

connect_database()

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.btn_start = tk.Button(self, text="Start", command=self.start_server)
        self.btn_start.pack(side="top")
        self.btn_stop = tk.Button(self, text="Stop", command=self.stop_server)
        self.btn_stop.pack(side="top")

        self.user_title = tk.Label(self, text="Users")
        self.user_title.pack(side="left")
        self.user_list = tk.Listbox(self)
        self.user_list.pack(side="left")
        self.btn_add_user = tk.Button(self, text="Add")
        self.btn_add_user.pack(side="left")
        self.btn_remove_user = tk.Button(self, text="Remove")
        self.btn_remove_user.pack(side="left")

        self.console = tkinter.scrolledtext.ScrolledText(self)
        self.console.pack(side="bottom")

    def start_server(self):
        self.console.insert(tk.END, "[%s] Starting server...\n" % time.ctime())

    def stop_server(self):
        self.console.insert(tk.END, "[%s] Stopping server...\n" % time.ctime())

root = tk.Tk()
root.title("SublimeTogetherServer")
app = Application(master=root)
app.mainloop()
