import json
from datetime import datetime, timedelta

# Load the eval_file JSON file
with open('task.json', 'r') as eval_file:
    questions = json.load(eval_file)

# The data is now a Python dictionary

# Load the eval_file JSON file
with open('answers-example.json', 'r') as answ_file:
    correct_answers = json.load(answ_file)


def p(dict):
    print(json.dumps(p, indent=2))


def dragCard(question, time, trainer="dragCard", level="/topic-02-sprachliche-mittel/block-01-Sprachliche-Mittel-A-K/level-01"):
    event = {
        "event": "score",
        "mistakes": 0,
        "actions" : [],
        "levelPuid": "",
        "round": 0,
        "trainer": trainer,
        "level": level,
        "atoms": [],
        "src": "jASh",
        "created": time,
        "inserted": time
    }

    output = {
        "event": event,
        "exists": False,
        "archive": True
    }

    return output


def listMatch(question, time, trainer="listMatch", level="/topic-02-sprachliche-mittel/block-01-Sprachliche-Mittel-A-K/level-01", round=0):
    event = {
        "event": "score",
        "mistakes": 0,
        "actions" : [],
        "levelPuid": "",
        "round": round,
        "trainer": trainer,
        "level": level,
        "atom": [],
        "src": "jASh",
        "created": time,
        "inserted": time
    }

    output = {
        "event": event,
        "exists": False,
        "archive": True
    }

    return output


def buttons(question, time, trainer="buttons", level="/topic-02-sprachliche-mittel/block-01-Sprachliche-Mittel-A-K/level-01", round=0, levelPuid=""):
    event = {
        "event": "score",
        "mistakes": 0,
        "actions" : [],
        "levelPuid": levelPuid,
        "round": round,
        "trainer": trainer,
        "level": level,
        "atom": [],
        "src": "jASh",
        "created": time,
        "inserted": time
    }




#def makeActions(question, trainer):
#    actions = []
#    return actions


def universal (
        question,
        time,
        level,
        levelPuid,
        position,
        round=0,
        mistakes=0
    ):

    trainer = question["trainer"]

    # actions = makeActions(question, trainer)



    if trainer == "dragCard":
        event = {
            "event": "score",
            "mistakes": mistakes,
            "actions" : [],
            "levelPuid": levelPuid,
            "round": round,
            "trainer": trainer,
            "level": level,
            # "atom": {},
            "atoms": question["atoms"],
            "src": "jASh",
            "created": format_time(time),
            "inserted": format_time(time)
        }

        actions_lst = []

        duration = 50

        for i, atom in enumerate(question["atoms"]):
            position += duration
            actions_lst.append({
                "atomIndex": i,
                "correct": True,
                "position": position,
                "duration": duration
            })

        event["actions"] = actions_lst

        output = {
            "event": event,
            "exists": False,
            "archive": True
        }

        outputs = [output]

    elif trainer == "listMatch":
        outputs = []

        for atom in question["atoms"]:
            event = {
                "event": "score",
                "mistakes": mistakes,
                "actions" : [],
                "levelPuid": levelPuid,
                "round": round,
                "trainer": trainer,
                "level": level,
                "atom": atom,
                # "atoms": [],
                "src": "jASh",
                "created": format_time(time),
                "inserted": format_time(time)
            }

            actions_lst = []

            duration = 50
            position += duration

            actions_lst.append({
                "text": f"'{atom['a']}' + '{atom['b']}'",
                "correct": True,
                "position": position,
                "duration": duration
            })

            event["actions"] = actions_lst

            output = {
                "event": event,
                "exists": False,
                "archive": True
            }

            outputs.append(output)
            

    elif trainer == "buttons":
        outputs = []

        for atom in question["atoms"]:
            event = {
                "event": "score",
                "mistakes": mistakes,
                "actions" : [],
                "levelPuid": levelPuid,
                "round": round,
                "trainer": trainer,
                "level": level,
                "atom": atom,
                # "atoms": [],
                "src": "jASh",
                "created": format_time(time),
                "inserted": format_time(time)
            }

            actions_lst = []

            duration = 50
            position += duration

            actions_lst.append({
                "text": atom["b"].rsplit(" ")[0][2:],
                "correct": True,
                "position": position,
                "duration": duration
            })

            event["actions"] = actions_lst

            output = {
                "event": event,
                "exists": False,
                "archive": True
            }

            outputs.append(output)

    return outputs



def format_time(time):
    return time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"


def answer_questions(questions):
    """Answer the questions in the questions dictionary and return a dictionary with the answers."""
    answers = []
    start_time = datetime.utcnow()
    global position
    position = 0

    levelPuid = questions["puid"]
    grade = levelPuid.rsplit("/")[0]
    level = questions["path"].rsplit(grade)[1]

    for question in questions["trainers"]:
        time = start_time + timedelta(seconds=position/10)
        answer = universal(question, time, level, levelPuid, position)
        # position += pos_delta
        answers += answer

    return answers



answers = answer_questions(questions)

print(answers)

# write to file
with open("answers.json", "w") as f:
    json.dump(answers, f, indent=4)
f.close()

# write to file (single line)
with open("answers-oneline.json", "w") as f:
    json.dump(answers, f)
f.close()