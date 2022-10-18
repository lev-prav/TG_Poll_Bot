import enum
import json


def read_json(file_name = "questions.json") -> list:
    with open(file_name, 'r') as quests:
        return json.load(quests)

class ANSWER_TYPES(enum.Enum):
    POSITIVE = 0
    NEGATIVE = 1

    def get_answer_by_value(index : int):
        answers = [ANSWER_TYPES.POSITIVE, ANSWER_TYPES.NEGATIVE]
        if index >= len(answers) or index < 0:
            raise Exception("Idi na hui")

        return answers[index]

class Answer:
    def __init__(self, ans: ANSWER_TYPES, user_id : int) -> None:
        self.ans = ans 
        self.user_id = user_id
    
    def to_str(self):
        return f"{self.ans.value};{self.user_id}"
    
    def from_str(data_str: str):
        ans_val, id = data_str.split(';')
        data = Answer(ANSWER_TYPES.get_answer_by_value(int(ans_val)), int(id))
        return data

class Question:
    order: int 
    text : str
    answers : list

    def __init__(self, quest : dict) -> None:
        self.__dict__ = quest

class EndOfPoll(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Poll:
    def __init__(self) -> None:
        self.quest_index = 0
        self.set_data()
        self.stop_chat = object()
    
    def next_question(self)-> Question:
        self.quest_index += 1
        if self.quest_index >= len(self.quests):
            self.stop_chat()
            raise Exception("End of Poll")
        
        return self.quests[self.quest_index]
    
    def receive_answer(self, answer : Answer):
        
        if answer.ans == ANSWER_TYPES.POSITIVE.value: 
            print("POSITIVE")
        elif answer.ans == ANSWER_TYPES.NEGATIVE.value:
            print("NEGATIVE")
        
        if self.quest_index in self.rules.keys():
            self.quest_index = self.rules[self.quest_index][answer.ans.value] - 1
    
    def set_data(self):
        data = read_json()
        self.quests = data["quests"]
        self.quests : dict = {quest["order"] : Question(quest) 
                                for quest in sorted(self.quests, key = lambda quest : quest["order"])}
        self.rules : dict = self.parse_rules(data["rules"])
    
    def reset(self):
        self.quest_index = 0
    
    def parse_rules(self, rules : dict):
        return {
            int(key) : {
                int(k) : int(v) 
                for k, v in val.items()
            }
            for key, val in rules.items()
        }
    