import telebot
from telebot import types
from Chat import Chat
from config import TOKEN
import threading

class TGBot:
    def __init__(self) -> None:
        self.bot = telebot.TeleBot(TOKEN)
        self.start = self.bot.message_handler(commands=["start"])(self.start)
        self.users = []
        self.chat = Chat(self.bot)

    
    def start(self, message):
        if message.from_user.id not in self.users:
            print("Add User")
            self.chat.add_user(message.from_user)
        
        self.chat.start(message.from_user)
    
    def run(self):
        self.bot.infinity_polling()