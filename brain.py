from tkinter.filedialog import askopenfile
import sqlite3
import random
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


data = []
all_chapters_data = []
quiz_data = []
current_question = []
current_question_answer = []


# --------------------------------- DATABASE OPERATIONS ----------------------------------------- #


def add_data_to_db_table(cur, category, title, question, answer):
    sqlite_insert_with_param = """INSERT INTO questions
                              (category, chapter, question, answer) 
                              VALUES (?, ?, ?, ?);"""
    data_tuple = (category, title, question, answer)
    cur.execute(sqlite_insert_with_param, data_tuple)


def delete_table():
    pass


# --------------------------------------- QUIZ -------------------------------------------------- #

# Loads chapters and categories to the Menu list section on left #
def load_chapters():
    chapters = []
    con = sqlite3.connect(resource_path("data.db"))
    cur = con.cursor()
    cur.execute("""SELECT * from questions""")
    content = cur.fetchall()

    for chapter in content:
        all_chapters_data.append(chapter)
        chapter_name = chapter[1]
        if chapter_name not in chapters:
            chapters.append(chapter_name)
    cur.close()
    return chapters


# load quiz questions related to selected chapters #
def fetch_chapter_questions(chapter):
    quiz_data.clear()
    chapter_name = chapter.get()
    if chapter_name != "Select Chapter":
        for item in all_chapters_data:
            if chapter_name == item[1]:
                q = item[2]
                a = item[3]
                q_a_set = (q, a)
                quiz_data.append(q_a_set)
        start_quiz(quiz_data)


# starts quiz by flashing first question on clicking quiz start button #
def start_quiz(question_list):
    global current_question, current_question_answer
    first_question = random.choice(question_list)
    current_question.append(first_question[0])
    current_question_answer.append(first_question[1])


# on clicking '/' button it flashes next question #
def next_question():
    current_question.clear()
    current_question_answer.clear()
    q_a = random.choice(quiz_data)
    next_q = q_a[0]
    next_a = q_a[1]
    current_question.append(next_q)
    current_question_answer.append(next_a)


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
    con = sqlite3.connect(resource_path("data.db"))
    cur = con.cursor()
    print(data)
    for i in data:
        if i != '':
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


