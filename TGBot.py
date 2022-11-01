import asyncio
import telebot
from telebot import types
from BD import DBClient
from Chat import Chat
from config import TOKEN
import threading

class TGBot:
    def __init__(self) -> None:
        self.bot = telebot.TeleBot(TOKEN)
        self.start = self.bot.message_handler(commands=["start"])(self.start)
        self.users = []
        self.db_client = DBClient()
        self.chat = Chat(self.bot, self.db_client)

    
    def start(self, message):
        if message.from_user.id not in self.users:
            print("Add User")
            self.chat.add_user(message.from_user)
        
        self.chat.start(message.from_user)
    
    def run(self):
        #asyncio.run(self.db_client.connect())
        self.bot.infinity_polling()