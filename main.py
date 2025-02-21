from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"

# Window Setup
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)


# Load Data
data = pandas.read_csv("data/french_words.csv") # data is now a DataFrame containing CSV data
# Converts the DataFrame into a list of dictionaries
data_dict = data.to_dict(orient="records")
print(data_dict)

# Function to Show a Random Card
def next_card():
    global current_card
    current_card = random.choice(data_dict)  # Pick a random word
    canvas.itemconfig(card_title, text="French")  # Update title text
    canvas.itemconfig(card_word, text=current_card["French"])  # Update word text

# Create Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
canvas.create_image(400, 263, image=card_front)

# Text on Canvas
card_title = canvas.create_text(400, 150, text="Title", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=(FONT_NAME, 60, "bold"))

canvas.grid(column=1, row=0, columnspan=2)

# Buttons
wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightthickness=0, command=next_card)
right_button.grid(column=2, row=1)

# Start with a Random Word
next_card()


window.mainloop()

