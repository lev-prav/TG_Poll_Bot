import enum
import json


def read_json(file_name = "questions.json") -> list:
    with open(file_name, 'r') as quests:
        return json.load(quests)

class ANSWER_TYPES(enum.Enum):
    NEGATIVE = 0
    POSITIVE = 1

    def get_answer_by_value(index : int):
        answers = [ANSWER_TYPES.NEGATIVE, ANSWER_TYPES.POSITIVE]
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

class Poll:
    def __init__(self) -> None:
        self.quest_index = 0
        data = read_json()
        self.quests = data["quests"]
        self.quests : dict = {quest["order"] : Question(quest) 
                                for quest in sorted(self.quests, key = lambda quest : quest["order"])}
        self.rules : dict = self.parse_rules(data["rules"])
    
    def next_question(self)-> Question:
        self.quest_index += 1

        return self.quests[self.quest_index]
    
    def receive_answer(self, answer : Answer):
        if answer.ans == ANSWER_TYPES.POSITIVE.value: 
            print("POSITIVE")
        elif answer.ans == ANSWER_TYPES.NEGATIVE.value:
            print("NEGATIVE")
        
        if answer.ans.value in self.rules.keys():
            
    
    def parse_rules(self, rules : dict):
        return {
            int(key) : {
                int(k) : int(v) 
                for k, v in val.items()
            }
            for key, val in rules.items()
        }
    