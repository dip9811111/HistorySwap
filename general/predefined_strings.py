import os
from dotenv import load_dotenv
from telegram import KeyboardButton


(START_NEW, HOME, CHOOSE_EVENT, CHOOSE_CHARACTER, CHOOSE_NUMBER_OF_IMAGES,
 CONFIRM_FIRST_PROMPT, GENERATE_IMAGE, GENERATE_CAPTION, SEND_TO_INSTAGRAM,
 MODIFY_DALLE_PROMPT, INSERT_MANUAL_DALLE_PROMPT,
 INSERT_MANUAL_GPT_PROMPT) = range(12)

str_event = "Find event of the day"
str_home = "Go back to Home"
str_modify_dalle = "Modify DALLE prompt"
str_cancel_everything = "CANCEL EVERYTHING"
str_generate_other_images = "GENERATE OTHER IMAGES"
str_how_many_images = "How many images do you want to generate?"
str_proceed_image_gen = "Do you want to proceed with image generation?"

start_button = [[KeyboardButton(str_event)]]
back_button = [[KeyboardButton(str_home)]]
list_options = ["YES", "NO", "MODIFY THIS PROMPT", "SKIP THIS PART"]
list_options_2 = ["YES", "NO", "CANCEL"]
list_options_3 = ["YES", "CANCEL EVERYTHING"]
list_options_4 = ["YES", str_generate_other_images, str_cancel_everything]
buttons_YES_or_NO_annulla = [
    [KeyboardButton(f"{val}")] for i, val in enumerate(list_options_2)
]
buttons_YES_or_NO_skip = [
    [KeyboardButton(f"{val}")] for i, val in enumerate(list_options)
]

buttons_last_confirm = [
    [KeyboardButton(f"{val}")] for i, val in enumerate(list_options_3)
]

buttons_instagram = [
    [KeyboardButton(f"{val}")] for i, val in enumerate(list_options_4)
]

numbers_ = [i for i in range(1, 9)]
numbers_.append(str_modify_dalle)
numbers_.append(str_cancel_everything)

buttons_number_of_images = [
    [KeyboardButton(f"{val}")] for i, val in enumerate(numbers_)
]

load_dotenv()
OPEN_AI_KEY = os.getenv("OPENAI_KEY")
MAIN_DIR = os.getenv("MAIN_DIR")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
