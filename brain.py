from tkinter.filedialog import askopenfile
import sqlite3

data = []

# --------------------------------- DATABASE OPERATIONS ----------------------------------------- #


def add_data_to_db_table(cur, category, title, question, answer):
    sqlite_insert_with_param = """INSERT INTO questions
                              (category, chapter, question, answer) 
                              VALUES (?, ?, ?, ?);"""
    data_tuple = (category, title, question, answer)
    cur.execute(sqlite_insert_with_param, data_tuple)


# def delete_table():
#     con = sqlite3.connect("data.db")
#     cur = con.cursor()
#     cur.execute("DELETE TABLE questions;")
#     con.commit()
#     con.close()


# --------------------------------------- QUIZ -------------------------------------------------- #


def load_chapters():
    pass


def select_chapter():
    pass


def start_quiz():
    pass


def show_answer():
    pass


def mark_wrong():
    pass


def next_question():
    pass


def score_counter():
    pass


# ------------------------------------ ADD CHAPTER ---------------------------------------------- #


def process_content():
    global data
    file = askopenfile(filetypes=[('Text Files', '*.txt')])
    if file is not None:
        content = file.read()
        data = content.split("\n")


def save_chapter(category, title):
    category = category.get()
    title = title.get()
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    print(data)
    for i in data:
        q = i.split(";")[0]
        a = i.split(";")[1]
        if q[0] == ' ':
            q = q.strip(q[0])
        if q[-1] == ' ':
            q = q.strip(q[-1])
        if a[0] == ' ':
            a = a.strip(a[0])
        if a[-1] == ' ':
            a = a.strip(a[-1])
        add_data_to_db_table(cur, category, title, q, a)
    con.commit()
    con.close()


# delete_table()
