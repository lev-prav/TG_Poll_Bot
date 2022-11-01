import telebot
from telebot import types
from TGBot import TGBot


class TGClient:
    def __init__(self) -> None:
        self.__bot = TGBot()
        

    def run(self):

        print("Let's start")
        
        self.__bot.run()
        
        print("Goodby")


