import asyncio
from pprint import pprint
import telebot 
from telebot import types
from BD import DBClient
from Poll import ANSWER_TYPES, Answer, Poll, Question

class Chat:
    def __init__(self, bot : telebot.TeleBot, db_client : DBClient) -> None:
        self.bot = bot 
        self.polls = {}
        self.callback_worker = self.bot.callback_query_handler(func= lambda call: True)(self.callback_worker)
        self.db_client = db_client
    
    def add_user(self,  user):
        self.polls[user.id] = Poll()
        self.polls[user.id].stop_chat = self.stop_handler(user)
    
    def start(self, user):
        self.polls[user.id].reset()
        self.ask_question(user, self.polls[user.id].next_question())
    
    def callback_worker(self, call):
        callback = Answer.from_str(call.data)

        self.polls[call.message.chat.id].receive_answer(callback)
        print(callback.ans)
        self.ask_question(call.message.chat, self.polls[call.message.chat.id].next_question())

    def stop_handler(self, user):
        #insertion_coroutine = None
        def stop_poll():
            # if insertion_coroutine is not None:
            #     await insertion_coroutine
            #     insertion_coroutine = None

            poll = self.polls[user.id]
            user_answers = {}
            user_answers["user_id"] = user.id
            user_answers["answers"] = poll.answers
            if len(poll.answers) > 0:
                # insertion_coroutine = asyncio.create_task(
                #     self.db_client.insert_poll_into(poll.poll_name, poll.answers)
                # )
                self.db_client.insert_poll_into(poll.poll_name, user_answers)
                pprint(user_answers)
                poll.answers = {}
            self.bot.send_message(user.id, "Благодарим за участие в нашем опросе !")
        return stop_poll
        
    
    def ask_question(self, user, question : Question):

        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_yes = types.InlineKeyboardButton(   text=question.answers[0], 
                                                callback_data= Answer(ANSWER_TYPES.POSITIVE, user.id).to_str()
                                                ) 
        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(     text=question.answers[1], 
                                                callback_data= Answer(ANSWER_TYPES.NEGATIVE, user.id).to_str()
                                                )
        keyboard.add(key_no)

        self.bot.send_message(user.id, text=question.text, reply_markup=keyboard)