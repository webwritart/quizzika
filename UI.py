import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from brain import *
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.iconbitmap(resource_path("Quizzika_icon.ico"))

        self.head = Head(self)

        self.menu = Menu(self)

        self.question = Question(self)

        self.setting = Setting(self)

        self.mainloop()


class Head(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=0.15)
        self.create_widgets()

    def create_widgets(self):
        heading = ttk.Label(self, text='QUIZZIKA', font=("Cinzel", 30), foreground='black')
        heading.place(relx=0.02, rely=0.2)


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(relief="ridge")
        self.place(x=0, rely=0.15, relwidth=0.25, relheight=0.85)

        options = load_chapters()
        options.insert(0, "Select Chapter")

        clicked = StringVar()

        self.chapters = ttk.OptionMenu(self, clicked, *options)
        self.chapters.grid(row=0, column=0, padx=(50, 0), pady=10)
        self.load_quiz = ttk.Button(self, text="Load quiz", command=lambda: fetch_chapter_questions(clicked.get()))
        self.load_quiz.grid(row=1, column=0, columnspan=2, padx=(50, 0), pady=10, sticky='w')


class Question(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(relief="ridge")
        self.place(relx=0.25, rely=0.15, relwidth=0.75, relheight=0.60, )

        self.score = 0
        self.total = 0

        def disable_mark_wrong_button():
            self.mark_wrong.config(state=tk.DISABLED)

        def enable_mark_wrong_button():
            self.mark_wrong.config(state=tk.NORMAL)

        def disable_finish_button():
            self.finish.config(state=tk.DISABLED)

        def enable_finish_button():
            self.finish.config(state=tk.NORMAL)

        def enable_start_quiz_button():
            self.start_quiz.config(state=tk.NORMAL)

        def disable_start_question_button():
            self.start_quiz.config(state=tk.DISABLED)

        def update_score():
            self.score_card.config(text=f'{self.score}/{self.total}')

        def start_quiz():
            if len(current_chapter) != 0:
                self.answer_label.config(text="")
                enable_finish_button()
                remaining_questions.clear()
                remaining_questions.append(len(quiz_data) - 1)
                total_questions.clear()
                total_questions.append(len(quiz_data))
                self.remaining_questions.config(text=f'Remaining questions: {remaining_questions[0]}/{total_questions[0]}')
                if len(current_question) != 0:
                    self.question_label.config(text=current_question[0])
                    self.total = 0
                    self.total += 1
                    update_score()
                con = sqlite3.connect(DATABASE_URI)
                cur = con.cursor()
                cur.execute("""SELECT * from highest_score""")
                high_score_list = cur.fetchall()
                for score in high_score_list:
                    if score[0] == current_chapter[0]:
                        highest_score.clear()
                        highest_score.append(score[1])
                    else:
                        highest_score.clear()
                con.close()
                if len(highest_score) != 0:
                    self.highest_score.config(text=f'Highest Score: {highest_score[0]}')
                else:
                    self.highest_score.config(text=f'Highest Score: ')
            else:
                messagebox.showwarning("warning", "Please Load quiz before Starting Quiz!")

        def update_answer():
            self.answer_label.config(text=current_question_answer[0])

        def next_q_a():

            if next_question() != "end":
                self.question_label.config(text=current_question[0])
                self.answer_label.config(text="")
                self.score += 1
                self.total += 1
                update_score()
                self.remaining_questions.config(text=f'Remaining questions: {remaining_questions[0]}/{total_questions[0]}')
            else:
                self.question_label.config(text="End of Quiz")
                self.answer_label.config(text="")
                self.remaining_questions.config(text=f'Remaining questions: None')

            enable_mark_wrong_button()

        def mark_wrong():
            self.score -= 1
            keep_question.clear()
            keep_question.append('True')
            disable_mark_wrong_button()

        def finish():
            self.score += 1
            score_percentage = (self.score/self.total)*100
            self.question_label.config(text=f'Congrats! You have scored {self.score} out of {self.total} | '
                                            f'Percentage: {score_percentage}')
            self.answer_label.config(text='')

            percentage = (self.score/self.total) * 100

            con = sqlite3.connect(DATABASE_URI)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS highest_score(chapter, highest_percentage)")
            cur.execute("""SELECT * from highest_score""")
            record = cur.fetchall()

            # if no previous record then create a new one
            if len(record) == 0:
                add_highest_record(cur, current_chapter[0], percentage)
            else:
                current_chapter_record_box = []
                # else search for previous record for the chapter if any, compare the score to the current,
                # update if higher,
                for r in record:
                    if r[0] == current_chapter[0]:
                        current_chapter_record_box.clear()
                        current_chapter_record_box.append(r)
                        current_record = r[1]
                        if percentage > current_record:
                            self.question_label.config(
                                text=f'Congrats! Record Made! {self.score} out of {self.total}')
                            delete_query = "DELETE FROM highest_score where chapter=?"
                            cur.execute(delete_query, (current_chapter[0],))
                            add_highest_record(cur, current_chapter[0], percentage)
                # if no record of current chapter found then create a fresh one.
                if len(current_chapter_record_box) == 0:
                    add_highest_record(cur, current_chapter[0], percentage)

            con.commit()
            con.close()
            con = sqlite3.connect(DATABASE_URI)
            cur = con.cursor()
            cur.execute("""SELECT * from highest_score""")
            highest_score_list = cur.fetchall()
            for score in highest_score_list:
                if score[0] == current_chapter[0]:
                    highest_score.clear()
                    highest_score.append(score[1])
            self.highest_score.config(text=f'Highest Score: {highest_score[0]}')

            con.close()
            reset_score()
            disable_finish_button()

        def reset_score():
            self.score = 0
            self.total = 0
            update_score()

        self.score_card = ttk.Label(self, text=f'{self.score}/{self.total}', font=("Cinzel", 30), foreground='black')
        self.score_card.place(relx=0.9, rely=0.05)
        self.highest_score = ttk.Label(self, text=f'Highest Score: ', font=("Calibri", 15))
        self.highest_score.grid(row=0, column=3)
        self.start_quiz = ttk.Button(self, text="Start Quiz", command=start_quiz)
        self.start_quiz.grid(row=0, column=0, pady=(50, 0), padx=80, sticky="w")
        self.remaining_questions = ttk.Label(self, text=f'remaining questions: ', font=("Calibri", 15))
        self.remaining_questions.grid(row=0, column=1)
        self.question_label = ttk.Label(self, text="", font=('Calibri', 30), wraplength=1100)
        self.question_label.grid(row=1, column=0, padx=80, pady=80, columnspan=5, sticky="w")
        self.answer_label = ttk.Label(self, text="", font=('calibri', 30), foreground='Green')
        self.answer_label.grid(row=2, column=0, columnspan=4, padx=80, sticky="w")
        self.answer_button = ttk.Button(self, text="Answer", command=update_answer)
        self.answer_button.grid(row=3, column=0, pady=50, padx=80, sticky="w")
        self.next = ttk.Button(self, text="Next", command=next_q_a)
        self.next.grid(row=3, column=1, padx=80, sticky="w")
        self.mark_wrong = ttk.Button(self, text="Mark Wrong", command=mark_wrong)
        self.mark_wrong.grid(row=3, column=2, padx=80, pady=50, sticky="w")
        self.finish = ttk.Button(self, text="Finish", command=finish)
        self.finish.grid(row=3, column=3, padx=80, sticky="w")
        self.reset_score = ttk.Button(self, text="Reset Score", command=reset_score)
        self.reset_score.grid(row=4, column=0, padx=80, sticky="w")


class Setting(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.25, rely=0.75, relwidth=0.75, relheight=0.25)
        self.config(borderwidth=1, border=True, )

        self.category = StringVar()
        self.title = StringVar()

        self.heading = ttk.Label(self, text="Add New Chapter", font=('Calibri', 20))
        self.file_upload = ttk.Button(self, text="Upload txt file", command=lambda: process_content(), width=40,
                                      padding=10)
        self.category_label = ttk.Label(self, text="Category", font=("Calibri", 20))
        self.category = ttk.Entry(self, textvariable=self.category, font=("Calibri", 20))
        self.title_label = ttk.Label(self, text="Title", font=("Calibri", 20))
        self.title = ttk.Entry(self, textvariable=self.title, font=("Calibri", 20))
        self.add = ttk.Button(self, text="Add Chapter", command=lambda: save_chapter(self.category, self.title),
                              width=150, padding=10)
        self.heading.grid(row=0, column=0, columnspan=2, padx=50, pady=0, sticky="w")
        self.file_upload.grid(row=1, column=0, columnspan=2, padx=70, pady=10, sticky="w")
        self.category_label.grid(row=2, column=0, padx=(70, 0), pady=10, sticky="w")
        self.category.grid(row=2, column=1, padx=0, pady=10, sticky="w")
        self.title_label.grid(row=2, column=2, padx=(30, 0), pady=10, sticky="e")
        self.title.grid(row=2, column=3, pady=10, sticky="w")
        self.add.grid(row=3, column=0, columnspan=4, sticky="w", padx=(30, 0), pady=10)
