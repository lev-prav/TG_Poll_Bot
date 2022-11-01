# TG_Quiz_Bot

I made this bot for polling people in research under the marketing project for portrait of the target audience. 
But i decided to make task a bit more complicated. 
So now (not now really, but soon) we have a program, wich you can load your own questions and quest graph, and got a ready for work PollBot.

Future plans:

- add an ability to load json quests in Telegram directly, without running program on user-computer

## Quest rules

There is an example of json file with all questions in poll. 

Threre you can see 3 main key's

1. poll_unique_name - your future database table will have this name and all the users passed THIS poll will be stored there. 
2. quests - paste here the list of questions you want to ask (details below)
3. rules - list of logical rules of your quest (details below)

## What is your Quest~~looks like~~ ?

{ <br>
    "order" : 1, <br>
    "text" : "Вы профессиональный музыкант?",<br>
    "answers" : ["Да","Нет"]<br>
}
<br><br>

- order - needs and ordinal of the question on your poll
- text - the quest
- answers - list of 2 answers positive at first position and negative at second 


## ~~same~~ Rules ~~apply~~

Example 


        "4":
        {
            "0" : 5, <br>
            "1" : 6 <br>
        }

Here "4" is an order key in the question in questions list. 
And 

if the answer is positive ("0"):


     you goes to the quest with the key 5,

else if answer is negative ("1"): 

    go to the 6 question