from book_tracker import book


class Interface:
    def __init__(self):
        self.books = []

    def run_loop(self):
        quit_flag = False
        while not quit_flag:
            print("test")
