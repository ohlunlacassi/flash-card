from tkinter import *
import pandas
import random

from debugpy.common.timestamp import current

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
current_card = {} # Store the current card
to_learn = {}

# Load Data
try:
    data = pandas.read_csv("data/words_to_learn.csv") # Load remaining words
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
    original_data.to_csv("data/words_to_learn.csv", index=False) # Save for future use
else:
    to_learn = data.to_dict(orient="records") # Converts to the list of dictionary

def next_card():
    """Show a random card."""
    global current_card # This statement is necessary because we need the same word to be accessible in both the next_card() and flip_card() functions
    global flip_timer

    # Cancel any previously scheduled flip to avoid overlapping timers
    window.after_cancel(flip_timer)

    current_card = random.choice(to_learn)  # Pick a random word

    # Reset to front image
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")  # Update title text
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")  # Update word text

    # Schedule the card to flip after 3 secs
    flip_timer = window.after(3000, flip_card)

def flip_card():
    """Flip the card to show the English translation."""
    canvas.itemconfig(canvas_image, image=card_back) # Change to card back image
    canvas.itemconfig(card_title, text="English", fill="white")  # Change title & color
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")  # Change word & color

def is_known():
    """Remove the current word from the list and update the CSV file."""
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# Window Setup
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# Create Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)

# Text on Canvas
card_title = canvas.create_text(400, 150, text="Title", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=(FONT_NAME, 60, "bold"))

canvas.grid(column=1, row=0, columnspan=2)

# Buttons
wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightthickness=0, command=is_known)
right_button.grid(column=2, row=1)

# Set an initial flip timer (needed to prevent errors if `next_card` isn't called immediately
flip_timer = window.after(3000, func=flip_card)

# Start with a Random Word
next_card()

window.mainloop()

