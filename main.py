from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from telegram.ext import Application
from support.handleChat import (
    startCommand,
    handle_Home,
    handle_ChooseEvent,
    handle_ChooseCharacter,
    handle_ConfirmFirstPrompt,
    handle_ChooseNumber,
    handle_GenerateImage,
    handle_GenerateCaption,
    handle_SendToInstagram,
    handle_ModifyDALLE_prompt,
    handle_InsertManualDallePrompt,
    handle_InserManualGPTPrompt
)
from general.predefined_strings import (
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
    TELEGRAM_TOKEN
)

application = Application.builder().token(TELEGRAM_TOKEN).build()

# Define the conversation handler
conversation_handler = ConversationHandler(
    # entry_points=[COMMANDHandler('start', startCOMMAND)],
    entry_points=[
        CommandHandler("start", startCommand),
        # MessageHandler(filters.text & ~filters.COMMAND, startCOMMAND),
        # Handle past users with any text
    ],
    states={
        HOME: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                              handle_Home)],
        CHOOSE_EVENT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND,
                           handle_ChooseEvent)
        ],
        CHOOSE_CHARACTER: [
            MessageHandler(filters.TEXT & ~filters.COMMAND,
                           handle_ChooseCharacter)
        ],
        CONFIRM_FIRST_PROMPT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND,
                           handle_ConfirmFirstPrompt)
        ],
        CHOOSE_NUMBER_OF_IMAGES: [
            MessageHandler(filters.TEXT & ~filters.COMMAND,
                           handle_ChooseNumber)
        ],
        GENERATE_IMAGE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND,
                           handle_GenerateImage)
        ],
        GENERATE_CAPTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND,
                           handle_GenerateCaption)
        ],
        SEND_TO_INSTAGRAM: [
            MessageHandler(filters.TEXT & ~filters.COMMAND,
                           handle_SendToInstagram)
        ],
        MODIFY_DALLE_PROMPT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND,
                           handle_ModifyDALLE_prompt)
        ],
        INSERT_MANUAL_DALLE_PROMPT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_InsertManualDallePrompt
            )
        ],
        INSERT_MANUAL_GPT_PROMPT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND,
                           handle_InserManualGPTPrompt)
        ],
    },
    fallbacks=[],
)

application.add_handler(conversation_handler)
print("Telegram is running...")
application.run_polling(1.0)
