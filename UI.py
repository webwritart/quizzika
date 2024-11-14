import tkinter as tk
from tkinter import ttk
from tkinter import *
from brain import process_content, save_chapter


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
        score = ttk.Label(self, text='9/10', font=("Cinzel", 30), foreground='black')
        score.place(relx=0.9, rely=0.2)


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, background='red').pack(expand=True, fill='both')
        self.place(x=0, rely=0.15, relwidth=0.25, relheight=0.85)


class Question(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.25, rely=0.15, relwidth=0.75, relheight=0.60)
        self.create_question_widgets()

    def create_question_widgets(self):
        c1 = tk.BooleanVar()
        c2 = tk.BooleanVar()
        c3 = tk.BooleanVar()
        c4 = tk.BooleanVar()
        question_label = ttk.Label(self, text="Question:", font=('Calibri', 30))
        question_label.grid(row=0, column=0, padx=80, pady=80)
        choice_1 = ttk.Checkbutton(self, text="choice 1", variable=c1)
        choice_2 = ttk.Checkbutton(self, text="choice 2", variable=c2)
        choice_3 = ttk.Checkbutton(self, text="choice 3", variable=c3)
        choice_4 = ttk.Checkbutton(self, text="choice 4", variable=c4)
        choice_1.grid(row=1, column=0)
        choice_2.grid(row=1, column=1)
        choice_3.grid(row=2, column=0)
        choice_4.grid(row=2, column=1)


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


App('QUIZZIKA', (1800, 1000))
