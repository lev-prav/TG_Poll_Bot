import telebot 
from telebot import types
from Poll import ANSWER_TYPES, Answer, Poll, Question

class Chat:
    def __init__(self, bot : telebot.TeleBot) -> None:
        self.bot = bot 
        self.polls = {}
        self.callback_worker = self.bot.callback_query_handler(func= lambda call: True)(self.callback_worker)
    
    def add_user(self,  user):
        self.polls[user.id] = Poll()
        self.polls[user.id].stop_chat = self.stop(user)
    
    def start(self, user):
        self.polls[user.id].reset()
        self.ask_question(user, self.polls[user.id].next_question())
    
    def callback_worker(self, call):
        callback = Answer.from_str(call.data)

        self.polls[call.message.chat.id].receive_answer(callback)
        print(callback.ans)
        self.ask_question(call.message.chat, self.polls[call.message.chat.id].next_question())

    def stop(self, user):
        def stop_poll():
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