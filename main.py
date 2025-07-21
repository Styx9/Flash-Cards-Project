from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
FLIP_DELAY = 3000
class FlashCardApp:
    def __init__(self):
        self.window = Tk()
        self.current_word = ""
        self.flip_timer = None
        self.to_learn = self._load_words()
        self._setup_ui()
    def _load_words(self):
        try:
            data = pandas.read_csv("data/french_words.csv")
            return {row.French:row.English for key,row in data.iterrows()}
        except FileNotFoundError:
            print("Words file not found! Check your data folder.")
            self.window.quit()
            return {}
    def _setup_ui(self):
            self.window.title("Flash Cards")
            self.window.config(background=BACKGROUND_COLOR, padx=50, pady=50)
            self.canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
            self.card_front = PhotoImage(file="images/card_front.png")
            self.card_back = PhotoImage(file="images/card_back.png")
            self.card_image = self.canvas.create_image(400, 263, image=self.card_front)
            self.language_text = self.canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
            self.word_in_fr = self.canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
            self.canvas.grid(column=0, row=0, columnspan=2)

            self.correct_btn_img = PhotoImage(file="images/right.png")
            self.correct_btn = Button(image=self.correct_btn_img, highlightthickness=0, cursor="hand2", command=self.handle_correct)
            self.correct_btn.grid(column=1, row=1)
            self.wrong_btn_img = PhotoImage(file="images/wrong.png")
            self.wrong_btn = Button(image=self.wrong_btn_img, highlightthickness=0, cursor="hand2", command=self.show_new_word)
            self.wrong_btn.grid(column=0, row=1)
    def update_card(self,word,language="French",image = None):
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)
        self.canvas.itemconfig(self.card_image, image=image)
        self.canvas.itemconfig(self.word_in_fr, text=word)
        self.canvas.itemconfig(self.language_text, text=language)
        if language == "French":
            self.flip_timer = self.window.after(FLIP_DELAY,self.flip_card)
    def flip_card(self):
        english_word = self.to_learn[self.current_word]
        self.update_card(word=english_word,language="English",image=self.card_back)
    def handle_correct(self):
        if self.current_word in self.to_learn:
           del self.to_learn[self.current_word]
        self.show_new_word()
    def show_new_word(self):
        if len(self.to_learn) > 0:
            self.current_word = random.choice(list(self.to_learn.keys()))
            self.update_card(self.current_word,image=self.card_front)
        else:
            self.update_card("No more cards!","You mastered French!")
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = FlashCardApp()
    app.run()