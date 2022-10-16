import telebot
from telebot import types
import threading
from TGBot import TGBot


class TGClient:
    def __init__(self) -> None:
        self.__bot = TGBot()
        

    def run(self):
        thread = threading.Thread(target= lambda : self.__bot.bot.polling(none_stop=True, interval=0))
        thread.start()

        input("PRESS ANY KEY\n")
        thread.join()


