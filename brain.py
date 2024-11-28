import sys
from tkinter.filedialog import askopenfile
import sqlite3
import random
import os

keep_question = ['False']
data = []
all_chapters_data = []
quiz_data = []
total_questions = []
remaining_questions = []
current_category = []
current_chapter = []
current_q_a = []
current_question = []
highest_score = []
current_question_answer = []
last_three_questions = []
user = os.getlogin()
STORAGE_FOLDER = "C:/Program Files/Quizzika"
# DATABASE_URI = STORAGE_FOLDER + '/data.db'
DATABASE_URI = "F:/data.db"
if not os.path.exists(STORAGE_FOLDER):
    os.mkdir(STORAGE_FOLDER)


# --------------------------------- APP OPERATIONS ---------------------------------------------- #

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# --------------------------------- DATABASE OPERATIONS ----------------------------------------- #


def add_highest_record(cur, title, highest_percentage):
    sqlite_insert_with_param = """INSERT INTO 
                                 highest_score (chapter, highest_percentage) 
                                  VALUES (?, ?);"""
    data_tuple = (title, highest_percentage)
    cur.execute(sqlite_insert_with_param, data_tuple)
    print('Updated New highest score record to the database')


def add_data_to_db_table(cur, category, title, question, answer):
    sqlite_insert_with_param = """INSERT INTO questions
                              (category, chapter, question, answer) 
                              VALUES (?, ?, ?, ?);"""
    data_tuple = (category, title, question, answer)
    cur.execute(sqlite_insert_with_param, data_tuple)
    print('Added new Chapter to the Database')


# def delete_table():
#     table_parameter = "{questions}"
#     drop_table_sql = f"DROP TABLE {table_parameter};"
#     get_tables_sql = "SELECT name FROM sqlite_schema WHERE type='table';"
#
#     def delete_all_tables(con):
#         tables = get_tables(con)
#         delete_tables(con, tables)
#
#     def get_tables(con):
#         cur = con.cursor()
#         cur.execute(get_tables_sql)
#         tables = cur.fetchall()
#         cur.close()
#         return tables
#
#     def delete_tables(con, tables):
#         cur = con.cursor()
#         for table, in tables:
#             sql = drop_table_sql.replace(table_parameter, table)
#             cur.execute(sql)
#         cur.close()
#
#         con = sqlite3.connect("data.db")
#         delete_all_tables(con)


# --------------------------------------- QUIZ -------------------------------------------------- #

# Loads chapters and categories to the Menu list section on left #
def load_chapters():
    chapters = []
    con = sqlite3.connect(DATABASE_URI)
    cur = con.cursor()
    cur.execute("""SELECT * from questions""")
    content = cur.fetchall()

    for chapter in content:
        all_chapters_data.append(chapter)
        chapter_name = chapter[1]
        if chapter_name not in chapters:
            chapters.append(chapter_name)

    con.close()
    print('Chapters loaded to the section Menu!')
    return chapters


# load quiz questions related to selected chapters #
def fetch_chapter_questions(chapter):
    current_chapter.clear()
    current_chapter.append(chapter)
    con = sqlite3.connect(DATABASE_URI)

    # Fetch questions from the database for the current selected chapter #
    cur = con.cursor()
    cur.execute("""SELECT * from questions""")
    content = cur.fetchall()
    keep_searching = True
    if keep_searching:
        for ch in content:
            if ch[1] == chapter:
                keep_searching = False
                category = ch[0]
                current_category.clear()
                current_category.append(category)

    con.close()

    quiz_data.clear()
    chapter_name = chapter
    if chapter_name != "Select Chapter":
        for item in all_chapters_data:
            if chapter_name == item[1]:
                q = item[2]
                a = item[3]
                q_a_set = (q, a)
                quiz_data.append(q_a_set)
        load_question(quiz_data)
    print('Quiz Data loaded successfully!')


# starts quiz by flashing first question on clicking quiz start button #
def load_question(question_list):
    global current_question, current_question_answer
    remaining_questions.clear()
    remaining_questions.append(len(quiz_data))
    first_question = random.choice(question_list)
    current_q_a.clear()
    current_q_a.append(first_question)
    current_question.clear()
    current_question_answer.clear()
    current_question.append(first_question[0])
    current_question_answer.append(first_question[1])

    # Update the current chapter's highest score #
    highest_score.clear()
    print('Questions for the current quiz loaded successfully!')


# on clicking '/' button it flashes next question #
def next_question():
    if len(quiz_data) != 0 and keep_question[0] == 'False':
        # print(current_q_a[0])
        # print(quiz_data)
        quiz_data.remove(current_q_a[0])
        remaining_questions.clear()
        remaining_questions.append(len(quiz_data) - 1)

    # Adding current questions to the recent questions list to help avoiding question repeat too quickly #
    if keep_question[0] == 'True':
        if remaining_questions[0] > 3:
            last_three_questions.append(current_question[0])
        else:
            last_three_questions.clear()
        if len(last_three_questions) > 3:
            del last_three_questions[0]
        print('Last wrong question stored in "quiz data" as well as "Recent questions"')

    current_question.clear()
    current_question_answer.clear()
    current_q_a.clear()
    keep_question.clear()
    keep_question.append('False')
    if len(quiz_data) != 0:
        q_a = random.choice(quiz_data)

        keep_matching = True
        while keep_matching:
            if q_a[0] in last_three_questions:
                print(q_a)
                q_a = random.choice(quiz_data)
                keep_matching = True
            else:
                keep_matching = False
        current_q_a.append(q_a)
        next_q = q_a[0]
        next_a = q_a[1]
        current_question.append(next_q)
        current_question_answer.append(next_a)
    else:
        return "end"

    print('Next question loaded successfully!')

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
    con = sqlite3.connect(DATABASE_URI)
    cur = con.cursor()
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

