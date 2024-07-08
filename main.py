from tkinter import *
import pandas
import random

# Variables
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
flip_timer = 3000

# Opening csv
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data_file = pandas.read_csv("./data/french_words.csv")
    to_learn = data_file.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    to_learn.remove(current_card)
    data_ = pandas.DataFrame(to_learn)
    data_.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# GUI
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Canvas
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

card_title = canvas.create_text(400, 150, text="", font=("Ariel", 30, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 50, "bold"))

# Buttons
right = PhotoImage(file="./images/right.png")
cross = PhotoImage(file="./images/wrong.png")

right_button = Button(image=right, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

cross_button = Button(image=cross, highlightthickness=0, command=next_card)
cross_button.grid(row=1, column=0)

next_card()

window.mainloop()
