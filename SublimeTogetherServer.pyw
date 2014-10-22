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

def query_sql(sql):
    '''Execute a sql clause and return the cursor'''
    global conn
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    return c

connect_database()

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.load_users()
        self.log("Standby.")

    def createWidgets(self):
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left")
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right")

        self.users_label = tk.Label(self.right_frame, text="Users")
        self.users_label.pack(side="top")
        self.users_list = tk.Listbox(self.right_frame, height=16)
        self.users_list.pack(side="top")
        self.manage_frame = tk.Frame(self.right_frame)
        self.manage_frame.pack(side="bottom")
        self.add_button = tk.Button(self.manage_frame, text="Add", command=self.add_user_dialog)
        self.add_button.pack(side="left")
        self.delete_button = tk.Button(self.manage_frame, text="Delete", command=self.delete_user)
        self.delete_button.pack(side="right")

        self.console = tkinter.scrolledtext.ScrolledText(self.left_frame, height=20, width=60)
        self.console.pack(side="top")
        self.control_button = tk.Button(self.left_frame, text="Start",
            command=self.control_server)
        self.control_button.pack(side="bottom")

    def load_users(self):
        c = query_sql("SELECT * FROM users ORDER BY username ASC")
        rows = c.fetchall()
        for row in rows:
            self.users_list.insert(tk.END, row[0])


    def log(self, text=""):
        self.console.insert(tk.END, "[%s] %s\n" % (time.strftime("%H:%M:%S"), text))

    def control_server(self):
        self.log("Controlling server...")

    def add_user_dialog(self):
        self.add_dialog = tk.Toplevel(self)

        left_side = tk.Frame(self.add_dialog)
        left_side.pack(side="left")
        right_side = tk.Frame(self.add_dialog)
        right_side.pack(side="left")

        username_label = tk.Label(left_side, text="Username")
        username_label.pack(side="top")
        self.username = tk.StringVar()
        self.username_input = tk.Entry(right_side, textvariable=self.username)
        self.username_input.pack(side="top")
        password_label = tk.Label(left_side, text="Password")
        password_label.pack(side="top")
        self.password = tk.StringVar()
        self.password_input = tk.Entry(right_side, textvariable=self.password, show='*')
        self.password_input.pack(side="top")

        confirm_button = tk.Button(self.add_dialog, text="Confirm", command=self.add_user)
        confirm_button.pack(side="right")

        self.add_dialog.focus_set()
        self.add_dialog.grab_set_global()
        self.add_dialog.transient(self)
        self.log("Add user...")

    def add_user(self):
        username = self.username.get()
        password = self.password.get()
        sql = "INSERT INTO users VALUES('%s', '%s')" % (username, password)
        if username is not None and password is not None:
            execute_sql(sql)
            self.log(sql)
            self.add_dialog.destroy()


    def delete_user(self):
        self.log("Delete user...")

root = tk.Tk()
root.title("SublimeTogetherServer")
app = Application(master=root)
app.mainloop()
