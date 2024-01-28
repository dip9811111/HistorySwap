from telegram import KeyboardButton


class HistoryEvent:
    def __init__(self):
        self.topic = ""
        self.date = 0
        self.prompt = ""
        self.image_urls = ""
        self.image_path = ""
        self.caption = ""
        self.character = ""
        self.DALLE_prompt = ""
        self.modified_prompt = False


def check_number_range(input_string):
    if input_string.isdigit():
        number = int(input_string)
        if 1 <= number < 9:
            return True
        else:
            return False
    else:
        return False


def DisplayListOfFacts(list_of_facts):
    message_ = ""
    list_button_facts = []
    possible_answers = []
    for fact in list_of_facts:
        message_ += f"<b>{fact['date']}</b> {fact['text']}\n\n"
        list_button_facts.append([KeyboardButton(f"{fact['date']} {fact['text']}")])
        possible_answers.append(f"{fact['date']} {fact['text']}")

    return message_, list_button_facts, possible_answers
