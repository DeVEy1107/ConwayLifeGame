import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        self.geometry("400x300")


if __name__ == "__main__":
    app = App()
    app.mainloop()