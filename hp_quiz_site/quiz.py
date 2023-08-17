import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hp_quiz_site.settings")
django.setup()

from tkinter import *
import tkinter as tk
from tkinter import messagebox as mb

from hp_quiz_app.models import Question, Options, Answer

root = tk.Tk()

root.title("Harry Potter kvíz játék")

app_width = 800
app_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)

root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

bg = PhotoImage(file="hpbguj.png")

my_canvas = Canvas(root, width=800, height=500)
my_canvas.pack(fill="both", expand=True)

my_canvas.create_image(0, 0, image=bg, anchor="nw")


class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.options = options
        self.question_index = 0

        self.kerdes_cimke = my_canvas.create_text(
            400, 100, text="", font=("Helvetica", 20), fill="light cyan"
        )

        self.megjelenit_kerdes()

    def megjelenit_kerdes(self):
        question = self.questions[self.question_index]
        options = Options.objects.get(question=question)

        my_canvas.itemconfig(self.kerdes_cimke, text=question.question)

        option_texts = [
            options.option_a,
            options.option_b,
            options.option_c,
            options.option_d,
        ]
        button_texts = ["A)", "B)", "C)", "D)"]

        for option_index in range(len(option_texts)):
            button_text = button_texts[option_index]

            button = Button(
                root,
                text=f"{button_text} {option_texts[option_index]}",
                width=30,
                relief=RAISED,
                borderwidth=4,
                font=("Helvetica", 12),
                background="light cyan",
                activebackground="Black",
                activeforeground="light cyan",
                cursor="hand2",
                command=lambda o=option_index: self.ellenoriz(o),
            )
            button_window = my_canvas.create_window(
                250, 200 + option_index * 60, anchor="nw", window=button
            )

    def ellenoriz(self, option_index):
        helyes_valasz = self.questions[self.question_index].correct_option
        question = self.questions[self.question_index]

        selected_option = ["A", "B", "C", "D"][option_index]

        if selected_option == helyes_valasz:
            self.score += 1

        answer = Answer(question=question, selected_option=selected_option)
        answer.save()

        self.question_index += 1

        if self.question_index < len(self.questions):
            my_canvas.itemconfig(self.kerdes_cimke, text="")
            self.megjelenit_kerdes()
        else:
            mb.showinfo("Eredmény", f"A játék véget ért. Pontszám: {self.score}")


# Lekérdezi a kérdéseket és válaszlehetőségeket a Django adatbázisból
questions = Question.objects.all()
options = [list(option.values()) for option in Options.objects.values()]


quiz = Quiz(questions)

root.mainloop()
