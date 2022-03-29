from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial
from random_word import RandomWords


class App:
    def __init__(self, root):
        # Field data
        self.root = root
        self.generate_word()
        self.correct_guesses = []
        self.incorrect_guesses = []
        self.remaining_guesses = 8

        # Window Settings
        self.root.title("Hangman")
        self.root.resizable(0, 0)
        ico = Image.open('images/pb.png')
        photo = ImageTk.PhotoImage(ico)
        self.root.wm_iconphoto(False, photo)

        # MENU BAR
        root.option_add('*tearOff', False)
        menubar = Menu(root)
        root.config(menu=menubar)
        file_menu = Menu(self.root)
        menubar.add_cascade(menu=file_menu, label="File")
        file_menu.add_command(label="New Game", command=self.reset)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)
        help_menu = Menu(self.root)
        menubar.add_cascade(menu=help_menu, label="Help")
        help_menu.add_command(
            label="About", command=lambda: messagebox.showinfo(
                title="About", message="Created by Peyton Bechard © 2022."))


        # TITLE AREA
        self.title_area = ttk.Frame(self.root, width=430, height=50, relief=RIDGE, padding=10)
        self.title_area.pack()
        self.title_area.pack_propagate(False)
        ttk.Label(self.title_area, text="H A N G M A N", font=("Arial", 18, "bold")).pack()

        # WORD AREA
        self.word_area = ttk.Frame(self.root, width=430, height=50, relief=RIDGE, padding=10)
        self.word_area.pack()
        self.word_area.pack_propagate(False)
        self.displayed_word = ttk.Label(self.word_area, text=len(self.word) * "_ ", font=24)
        self.displayed_word.pack()

        # PLAY AREA
        self.play_area = ttk.Frame(self.root)
        self.play_area.pack()
        # Guesses Area
        self.guesses_area = ttk.Frame(self.play_area, width=215, height=250, relief=RIDGE, padding=20)
        self.guesses_area.pack(side=LEFT)
        self.guesses_area.pack_propagate(False)
        ttk.Label(self.guesses_area, text="Correct: ", font=("Arial", 12, "bold")).pack(anchor=W)
        self.correct = ttk.Label(self.guesses_area, text="", foreground="green", font=8)
        self.correct.pack(anchor=W)
        ttk.Label(self.guesses_area, text="Incorrect: ", font=("Arial", 12, "bold")).pack(anchor=W)
        self.incorrect = ttk.Label(self.guesses_area, text="", foreground="red", font=8)
        self.incorrect.pack(anchor=W)
        ttk.Label(self.guesses_area, text="Guesses left: ", font=("Arial", 12, "bold")).pack(anchor=W)
        self.remaining = ttk.Label(self.guesses_area, text=self.remaining_guesses, foreground="green", font=8)
        self.remaining.pack(anchor=W)

        # Picture Area
        self.hangman_area = ttk.Frame(self.play_area, width=215, height=250, relief=RIDGE, padding=30)
        self.hangman_area.pack(side=LEFT)
        self.hangman_area.grid_propagate(False)
        ttk.Label(self.hangman_area, text="|").grid(row=1, column=8)
        ttk.Label(self.hangman_area, text="_").grid(row=0, column=8)
        ttk.Label(self.hangman_area, text="_").grid(row=0, column=7)
        ttk.Label(self.hangman_area, text="_").grid(row=0, column=6)
        ttk.Label(self.hangman_area, text="_").grid(row=0, column=5)
        ttk.Label(self.hangman_area, text="_").grid(row=0, column=4)
        ttk.Label(self.hangman_area, text="_").grid(row=0, column=3)
        ttk.Label(self.hangman_area, text="_").grid(row=0, column=2)
        ttk.Label(self.hangman_area, text="_").grid(row=0, column=1)
        ttk.Label(self.hangman_area, text="|").grid(row=1, column=1)
        ttk.Label(self.hangman_area, text="|").grid(row=2, column=1)
        ttk.Label(self.hangman_area, text="|").grid(row=3, column=1)
        ttk.Label(self.hangman_area, text="|").grid(row=4, column=1)
        ttk.Label(self.hangman_area, text="|").grid(row=5, column=1)
        ttk.Label(self.hangman_area, text="|").grid(row=6, column=1)
        ttk.Label(self.hangman_area, text="__").grid(row=6, column=0)
        ttk.Label(self.hangman_area, text="__").grid(row=6, column=2)
        ttk.Label(self.hangman_area, text=" ").grid(row=7, column=0)

        # COMMAND AREA
        self.command_area = ttk.Frame(self.root, relief=RIDGE)
        self.command_area.pack()
        # Creates letter buttons
        for i in range(0, 25):
            ttk.Button(self.command_area, text=chr(97+i), command=partial(self.guess, chr(97+i)))\
                .grid(row=(i//5), column=i%5, padx=5, pady=5)
        ttk.Button(self.command_area, text="z", command=partial(self.guess, "z"))\
            .grid(row=6, column=2, padx=5, pady=5)

    def generate_word(self):
        try:
            self.word = RandomWords().get_random_word(minCorpusCount=2500, minLength=5, maxLength=8).lower()
        except:
            messagebox.showerror(title="Error", message="Unable to connect. Please try again.")
            self.root.quit()
        while True:
            if self.test_word():
                break

    def test_word(self):
        for letter in self.word:
            if not letter.isalpha:
                self.word = RandomWords().get_random_word(minCorpusCount=2500, minLength=5, maxLength=8).lower()
                return False
        return True

    def guess(self, letter):
        if letter in self.word and letter not in self.correct_guesses:
            self.correct_guesses.append(letter)
        elif letter not in self.word and letter not in self.incorrect_guesses:
            self.incorrect_guesses.append(letter)
            self.remaining_guesses -= 1
        self.update_screen()

    def update_screen(self):
        self.update_word()
        self.update_guesses()
        self.update_hangman()

    def update_word(self):
        result = ""
        for letter in self.word:
            if letter in self.correct_guesses:
                result += letter.upper() + " "
            else:
                result += "_ "
        self.displayed_word.config(text=result, foreground="black")
        if "_" not in self.displayed_word["text"]:
            self.displayed_word.config(foreground="green")
            play_again = messagebox.askyesno(title="You win!", message="You win! Play again?")
            if play_again:
                self.reset()
            else:
                self.root.quit()

    def update_guesses(self):
        correct_list = ", ".join(self.correct_guesses)
        incorrect_list = ", ".join(self.incorrect_guesses)
        self.correct.config(text=correct_list)
        self.incorrect.config(text=incorrect_list)
        self.remaining.config(text=self.remaining_guesses)

    def update_hangman(self):
        if self.remaining_guesses == 0:
            ttk.Label(self.hangman_area, text="\\").grid(row=6, column=9)
            self.game_over()
        elif self.remaining_guesses == 1:
            ttk.Label(self.hangman_area, text="/").grid(row=6, column=7)
        elif self.remaining_guesses == 2:
            ttk.Label(self.hangman_area, text="|").grid(row=5, column=8)
        elif self.remaining_guesses == 3:
            ttk.Label(self.hangman_area, text="|").grid(row=4, column=8)
            self.remaining.config(foreground="red")
        elif self.remaining_guesses == 4:
            ttk.Label(self.hangman_area, text="_").grid(row=3, column=9)
            ttk.Label(self.hangman_area, text="_").grid(row=3, column=10)
        elif self.remaining_guesses == 5:
            ttk.Label(self.hangman_area, text="_").grid(row=3, column=6)
            ttk.Label(self.hangman_area, text="_").grid(row=3, column=7)
            self.remaining.config(foreground="orange")
        elif self.remaining_guesses == 6:
            ttk.Label(self.hangman_area, text="|").grid(row=3, column=8)
        elif self.remaining_guesses == 7:
            ttk.Label(self.hangman_area, text="0").grid(row=2, column=8)

    def game_over(self):
        self.displayed_word.config(text=self.word.upper(), foreground="red")
        play_again = messagebox.askyesno(title="You lose!", message=f"You lose! The word was {self.word.upper()}.\nPlay again?")
        if play_again:
            self.reset()
        else:
            self.root.destroy()

    def reset(self):
        self.generate_word()
        self.correct_guesses = []
        self.incorrect_guesses = []
        self.remaining_guesses = 8
        self.remaining.config(foreground="green")
        self.update_screen()
        ttk.Label(self.hangman_area, text=" ").grid(row=6, column=9)
        ttk.Label(self.hangman_area, text=" ").grid(row=6, column=7)
        ttk.Label(self.hangman_area, text=" ").grid(row=5, column=8)
        ttk.Label(self.hangman_area, text=" ").grid(row=4, column=8)
        ttk.Label(self.hangman_area, text=" ").grid(row=4, column=7)
        ttk.Label(self.hangman_area, text=" ").grid(row=4, column=6)
        ttk.Label(self.hangman_area, text=" ").grid(row=3, column=9)
        ttk.Label(self.hangman_area, text=" ").grid(row=3, column=10)
        ttk.Label(self.hangman_area, text=" ").grid(row=3, column=6)
        ttk.Label(self.hangman_area, text=" ").grid(row=3, column=7)
        ttk.Label(self.hangman_area, text=" ").grid(row=3, column=8)
        ttk.Label(self.hangman_area, text=" ").grid(row=2, column=8)


def main():
    root = Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
