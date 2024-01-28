from telegram import *
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
from requests import *
from telegram.ext import *


from general.predefined_strings import (
    START_NEW,
    HOME,
    CHOOSE_EVENT,
    CHOOSE_CHARACTER,
    CHOOSE_NUMBER_OF_IMAGES,
    CONFIRM_FIRST_PROMPT,
    GENERATE_IMAGE,
    GENERATE_CAPTION,
    SEND_TO_INSTAGRAM,
    MODIFY_DALLE_PROMPT,
    INSERT_MANUAL_DALLE_PROMPT,
    INSERT_MANUAL_GPT_PROMPT,
)
from general.predefined_strings import (
    back_button,
    buttons_instagram,
    buttons_YES_or_NO_annulla,
    buttons_YES_or_NO_skip,
    buttons_last_confirm,
    buttons_number_of_images,
    start_button,
    str_cancel_everything,
    str_event,
    str_generate_other_images,
    str_home,
    str_how_many_images,
    str_modify_dalle,
    str_proceed_image_gen
)

from general.utils import (
    HistoryEvent,
    check_number_range,
    DisplayListOfFacts
)

from support.fact_of_the_day import find_facts
from support.CallGPT import UseGPT
from support.GenerateImage import create_image

from telegram import InputFile
from datetime import datetime
from telegram.constants import ParseMode


async def startCommand(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text="Welcome to the DipoBot ☺️",
        reply_markup=ReplyKeyboardMarkup(start_button),
    )
    chat_id = update.effective_chat.id
    return HOME


async def handle_Home(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id

    if message_text == str_event:
        context.user_data["responses"] = HistoryEvent()
        list_of_facts = find_facts()
        message_, list_button_facts, possible_answers = DisplayListOfFacts(
            list_of_facts
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text=message_,
            reply_markup=ReplyKeyboardMarkup(list_button_facts),
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text="What event do you want to publish?",
            reply_markup=ReplyKeyboardMarkup(list_button_facts),
            parse_mode=ParseMode.HTML,
        )
        context.user_data["Opzioni_History_Event"] = possible_answers
        context.user_data["Complete_History_Events"] = list_of_facts

    return CHOOSE_EVENT


async def handle_ChooseEvent(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id

    possible_answers = context.user_data["Opzioni_History_Event"]

    if any(message_text[:125] == element[:125] for element in possible_answers):
        index_event = next(i for i, answer in enumerate(possible_answers) if message_text[:125] == answer[:125])
        complete_list_of_facts = context.user_data["Complete_History_Events"]
        event_ = complete_list_of_facts[index_event]
        context.user_data["responses"].date = event_["date"]
        context.user_data["responses"].topic = event_["text"]
        await context.bot.send_message(
            chat_id=chat_id,
            text="Insert the swap element",
            reply_markup=ReplyKeyboardMarkup(back_button),
            parse_mode=ParseMode.HTML,
        )
        return CHOOSE_CHARACTER
    else:
        return CHOOSE_EVENT


async def handle_ChooseCharacter(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id
    if message_text != str_home:
        context.user_data["responses"].swap_character = message_text
        topic = context.user_data["responses"].topic
        prompt_ = f"""I have to write a prompt to use GPT4 Image generation about the following topic:

Topic: {topic}

But I want that instead of the main character(s), there is/are {context.user_data['responses'].swap_character}.
Write me the prompt to send, in the format: 
PROMPT: """

        context.user_data["responses"].prompt = prompt_
        await context.bot.send_message(
            chat_id=chat_id,
            text="<b>The following PROMPT has been generated:</b>",
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_message(
            chat_id=chat_id, text=f"{prompt_}", parse_mode=ParseMode.HTML
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text="Do you want to confirm the prompt?",
            reply_markup=ReplyKeyboardMarkup(buttons_YES_or_NO_skip),
            parse_mode=ParseMode.HTML,
        )
        return CONFIRM_FIRST_PROMPT
    else:
        return HOME


async def handle_ConfirmFirstPrompt(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id

    if message_text == "YES" or context.user_data["responses"].modified_prompt:
        if not context.user_data["responses"].modified_prompt:
            prompt_ = context.user_data["responses"].prompt
            DALLE_prompt = UseGPT(prompt_, type_prompt="Prompt_for_image")
            context.user_data["responses"].DALLE_prompt = DALLE_prompt
        else:
            DALLE_prompt = context.user_data["responses"].DALLE_prompt
        await context.bot.send_message(
            chat_id=chat_id,
            text=DALLE_prompt,
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=str_how_many_images,
            reply_markup=ReplyKeyboardMarkup(buttons_number_of_images),
            parse_mode=ParseMode.HTML,
        )
        return CHOOSE_NUMBER_OF_IMAGES

    elif message_text == "NO":
        list_of_facts = context.user_data["Complete_History_Events"]
        message_, list_button_facts, _ = DisplayListOfFacts(
            list_of_facts
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=message_,
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text="What event do you want to publish?",
            reply_markup=ReplyKeyboardMarkup(list_button_facts),
            parse_mode=ParseMode.HTML,
        )
        return CHOOSE_EVENT

    elif message_text == "MODIFY THIS PROMPT":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Insert prompt to pass to GPT 3.5",
            parse_mode=ParseMode.HTML,
        )
        return INSERT_MANUAL_GPT_PROMPT

    elif message_text == "SKIP THIS PART":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Insert directly DALLE prompt",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("CANCEL")]]),
            parse_mode=ParseMode.HTML,
        )
        return INSERT_MANUAL_DALLE_PROMPT


async def handle_ChooseNumber(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id

    if check_number_range(message_text):
        context.user_data["responses"].number_of_images = int(message_text)
        await context.bot.send_message(
            chat_id=chat_id,
            text=str_proceed_image_gen,
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(buttons_last_confirm),
        )
        return GENERATE_IMAGE
    elif message_text == str_modify_dalle:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Insert modified DALLE PROMPT",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("CANCEL")]]),
            parse_mode=ParseMode.HTML,
        )
        return MODIFY_DALLE_PROMPT

    elif message_text == str_cancel_everything:
        await context.bot.send_message(
            chat_id=chat_id,
            text="All canceled. Do you want to try a new event?",
            reply_markup=ReplyKeyboardMarkup(start_button),
            parse_mode=ParseMode.HTML,
        )
        return HOME
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{str_how_many_images} Use the predefined buttons to answer",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(buttons_number_of_images),
        )
        return CHOOSE_NUMBER_OF_IMAGES


async def handle_InserManualGPTPrompt(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id

    if message_text != "CANCEL":
        chat_gpt_prompt = message_text
        context.user_data["responses"].prompt = chat_gpt_prompt
        await context.bot.send_message(
            chat_id=chat_id,
            text="<b>The PROMPT has been modified to:</b>",
            parse_mode=ParseMode.HTML,
        )

        await context.bot.send_message(
            chat_id=chat_id, text=f"{chat_gpt_prompt}", parse_mode=ParseMode.HTML
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text="Do you want to confirm the prompt?",
            reply_markup=ReplyKeyboardMarkup(buttons_YES_or_NO_skip),
            parse_mode=ParseMode.HTML,
        )
        return CONFIRM_FIRST_PROMPT

    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="What do you want to do?",
            reply_markup=ReplyKeyboardMarkup(start_button),
        )
        return HOME


async def handle_InsertManualDallePrompt(
    update: Update, context: CallbackContext
) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id

    if message_text != "CANCEL":
        DALLE_prompt = message_text
        context.user_data["responses"].DALLE_prompt = DALLE_prompt
        await context.bot.send_message(
            chat_id=chat_id,
            text=DALLE_prompt,
            parse_mode=ParseMode.HTML,
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text=str_proceed_image_gen,
            reply_markup=ReplyKeyboardMarkup(buttons_YES_or_NO_annulla),
            parse_mode=ParseMode.HTML,
        )
        return GENERATE_IMAGE
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="What do you want to do?",
            reply_markup=ReplyKeyboardMarkup(start_button),
        )
        return HOME


async def handle_GenerateImage(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id
    if message_text == "YES":
        DALLE_prompt = context.user_data["responses"].DALLE_prompt
        n_images = context.user_data["responses"].number_of_images
        url_images, path_images = create_image(DALLE_prompt, n_images)
        context.user_data["responses"].image_urls = url_images
        context.user_data["responses"].image_paths = path_images

        for path_image in path_images:
            with open(path_image, "rb") as photo:
                await context.bot.send_photo(chat_id=chat_id, photo=InputFile(photo))

        await context.bot.send_message(
            chat_id=chat_id,
            text="Do you want to generate the caption for the Instagram post?",
            reply_markup=ReplyKeyboardMarkup(buttons_instagram),
            parse_mode=ParseMode.HTML,
        )
        return GENERATE_CAPTION
    elif message_text == str_cancel_everything:
        await context.bot.send_message(
            chat_id=chat_id,
            text="All canceled. Do you want to try a new event?",
            reply_markup=ReplyKeyboardMarkup(start_button),
            parse_mode=ParseMode.HTML,
        )
        return HOME


async def handle_ModifyDALLE_prompt(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id
    if message_text != "CANCEL":
        context.user_data["responses"].DALLE_prompt = message_text
        context.user_data["responses"].modified_prompt = True
        await context.bot.send_message(
            chat_id=chat_id,
            text=context.user_data["responses"].DALLE_prompt,
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=str_how_many_images,
            reply_markup=ReplyKeyboardMarkup(buttons_number_of_images),
            parse_mode=ParseMode.HTML,
        )
        return CHOOSE_NUMBER_OF_IMAGES

        # url_image, path_image = create_image(message_text)
        # context.user_data["responses"].image_url = url_image
        # context.user_data["responses"].image_path = path_image
        # with open(path_image, "rb") as photo:
        #     await context.bot.send_photo(chat_id=chat_id, photo=InputFile(photo))
        # await context.bot.send_message(
        #     chat_id=chat_id,
        #     text="Do you want to generate the caption for the Instagram post?",
        #     reply_markup=ReplyKeyboardMarkup(buttons_YES_or_NO_annulla),
        #     parse_mode=ParseMode.HTML,
        # )
        # return GENERATE_CAPTION
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="What do you want to do?",
            reply_markup=ReplyKeyboardMarkup(start_button),
        )
        return HOME


async def handle_GenerateCaption(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id
    if message_text == "YES":
        prompt_for_caption = f"""Write a description of this event:

{context.user_data['responses'].date} {context.user_data['responses'].topic}

For an instagram page talking about historical events of the day, showing AI generated images.
"""
        instagram_caption = UseGPT(
            prompt_for_caption, type_prompt="Prompt_for_instagram"
        )
        current_date = datetime.now()
        formatted_date = current_date.strftime("%B %d")
        formatted_date = f"{formatted_date}, {context.user_data['responses'].date}"
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{formatted_date}\n\n{instagram_caption}",
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text="Is everything ok?",
            reply_markup=ReplyKeyboardMarkup(buttons_instagram),
            parse_mode=ParseMode.HTML,
        )

        return SEND_TO_INSTAGRAM
    elif message_text == str_generate_other_images:
        await context.bot.send_message(
            chat_id=chat_id,
            text=str_how_many_images,
            reply_markup=ReplyKeyboardMarkup(buttons_number_of_images),
            parse_mode=ParseMode.HTML,
        )
        return CHOOSE_NUMBER_OF_IMAGES
    elif message_text == str_cancel_everything:
        await context.bot.send_message(
            chat_id=chat_id,
            text="What do you want to do?",
            reply_markup=ReplyKeyboardMarkup(start_button),
            parse_mode=ParseMode.HTML,
        )
        return HOME


async def handle_SendToInstagram(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    chat_id = update.effective_chat.id
    if message_text == "YES":
        await context.bot.send_message(
            chat_id=chat_id,
            text="See you tomorrow for the next generation!",
            reply_markup=ReplyKeyboardMarkup(start_button),
            parse_mode=ParseMode.HTML,
        )
        return HOME
    elif message_text == "GENERATE OTHER IMAGES":
        await context.bot.send_message(
            chat_id=chat_id,
            text="See you tomorrow for the next generation!",
            reply_markup=ReplyKeyboardMarkup(buttons_number_of_images),
            parse_mode=ParseMode.HTML,
        )
        return CHOOSE_NUMBER_OF_IMAGES
    elif message_text == str_cancel_everything:
        await context.bot.send_message(
            chat_id=chat_id,
            text="What do you want to do?",
            reply_markup=ReplyKeyboardMarkup(start_button),
            parse_mode=ParseMode.HTML,
        )
        return HOME
