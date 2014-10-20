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
        self.log("Standby.")

    def createWidgets(self):
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left")
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right")

        self.users_label = tk.Label(self.right_frame, text="Onlines")
        self.users_label.pack(side="top")
        self.users_list = tk.Listbox(self.right_frame, height=16)
        self.users_list.pack(side="top")
        self.manage_frame = tk.Frame(self.right_frame)
        self.manage_frame.pack(side="bottom")
        self.add_button = tk.Button(self.manage_frame, text="Add", command=self.add_user)
        self.add_button.pack(side="left")
        self.delete_button = tk.Button(self.manage_frame, text="Delete", command=self.delete_user)
        self.delete_button.pack(side="right")

        self.console = tkinter.scrolledtext.ScrolledText(self.left_frame, height=20, width=60)
        self.console.pack(side="top")
        self.control_button = tk.Button(self.left_frame, text="Start",
            command=self.control_server)
        self.control_button.pack(side="bottom")

    def log(self, text=""):
        self.console.insert(tk.END, "[%s] %s\n" % (time.strftime("%H:%M:%S"), text))

    def control_server(self):
        self.log("Controlling server...")

    def add_user(self):
        self.log("Add user...")

    def delete_user(self):
        self.log("Delete user...")

root = tk.Tk()
root.title("SublimeTogetherServer")
app = Application(master=root)
app.mainloop()
