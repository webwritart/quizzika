import tkinter as tk
from tkinter import ttk
from tkinter import *
from brain import *


class App(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])

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
        self.load_quiz = ttk.Button(self, text="Load quiz", command=lambda: fetch_chapter_questions(clicked))
        self.load_quiz.grid(row=1, column=0, padx=(50, 0), pady=10)


class Question(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(relief="ridge")
        self.place(relx=0.25, rely=0.15, relwidth=0.75, relheight=0.60,)

        self.score = 0
        self.total = 0

        def update_score():
            self.score_card.config(text=f'{self.score}/{self.total}')

        def update_question():
            if len(current_question) != 0:
                self.question_label.config(text=current_question[0])
                self.total += 1
                update_score()

        def update_answer():
            self.answer_label.config(text=current_question_answer[0])

        def next_q_a():
            next_question()
            self.question_label.config(text=current_question[0])
            self.answer_label.config(text="")
            self.score += 1
            self.total += 1
            update_score()

        def mark_wrong():
            self.score -= 1

        def finish():
            self.score += 1
            self.question_label.config(text=f'Congrats! You have scored {self.score} out of {self.total}')
            self.answer_label.config(text='')
            update_score()

        def reset_score():
            self.score = 0
            self.total = 0
            update_score()

        self.score_card = ttk.Label(self, text=f'{self.score}/{self.total}', font=("Cinzel", 30), foreground='black')
        self.score_card.place(relx=0.9, rely=0.05)
        self.start_quiz = ttk.Button(self, text="Start Quiz", command=update_question)
        self.start_quiz.grid(row=0, column=0, pady=(50, 0))
        self.question_label = ttk.Label(self, text="", font=('Calibri', 30))
        self.question_label.grid(row=1, column=0, padx=80, pady=80, columnspan=4, sticky="w")
        self.answer_label = ttk.Label(self, text="", font=('calibri', 30), foreground='Green')
        self.answer_label.grid(row=2, column=0)
        self.answer_button = ttk.Button(self, text="Answer", command=update_answer)
        self.answer_button.grid(row=3, column=0, padx=80, pady=50)
        self.next = ttk.Button(self, text="Next", command=next_q_a)
        self.next.grid(row=3, column=1)
        self.mark_wrong = ttk.Button(self, text="Mark Wrong", command=mark_wrong)
        self.mark_wrong.grid(row=3, column=2, padx=80, pady=50)
        self.finish = ttk.Button(self, text="Finish", command=finish)
        self.finish.grid(row=3, column=3)
        self.reset_score = ttk.Button(self, text="Reset Score", command=reset_score)
        self.reset_score.grid(row=4, column=0)


class Setting(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.25, rely=0.75, relwidth=0.75, relheight=0.25)
        self.config(borderwidth=1, border=True, )

        self.category = StringVar()
        self.title = StringVar()

        self.heading = ttk.Label(self, text="Add New Chapter", font=('Calibri', 20))
        self.file_upload = ttk.Button(self, text="Upload txt file", command=lambda: process_content(), width=40, padding=10)
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


