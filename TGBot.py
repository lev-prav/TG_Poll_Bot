import telebot
from telebot import types
from config import TOKEN
from Poll import Question, Poll, ANSWER_TYPES, Answer

class TGBot:
    def __init__(self) -> None:
        self.bot = telebot.TeleBot(TOKEN)
        self.quiz = Poll()
        self.user_id = 0
        self.start = self.bot.message_handler(commands=["start"])(self.start)
        self.callback_worker = self.bot.callback_query_handler(func= lambda call: True)(self.callback_worker)
    
    def start(self, message):
        self.user_id = message.from_user.id
        self.bot.send_message(message.from_user.id, "Благодарим за участие в нашем опросе !")
        self.ask_question(self.quiz.next_question())

    def callback_worker(self, call):
        callback = Answer.from_str(call.data)

        self.quiz.receive_answer(callback)
        print(callback.ans)
        self.ask_question(self.quiz.next_question())
        
    
    def ask_question(self, question : Question):

        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_yes = types.InlineKeyboardButton(   text=question.answers[0], 
                                                callback_data= Answer(ANSWER_TYPES.POSITIVE, self.user_id).to_str()
                                                ) 
        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(     text=question.answers[1], 
                                                callback_data= Answer(ANSWER_TYPES.NEGATIVE, self.user_id).to_str()
                                                )
        keyboard.add(key_no)

        self.bot.send_message(self.user_id, text=question.text, reply_markup=keyboard)