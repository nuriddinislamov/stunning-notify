import os
import dotenv
import logging
from telegram.ext import (Updater,
                          CommandHandler,
                          ConversationHandler, MessageHandler, Filters, PicklePersistence)
from src.components import start


dotenv.load_dotenv()

# Set Debug to False when in production!
DEBUG = os.environ.get('DEBUG', True)


logging.basicConfig(
    filename='logs.log' if not DEBUG else None,
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if DEBUG else logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    pers = PicklePersistence(filename='PERSISTENCE')

    updater = Updater(os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher

    main_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', start.start),
            CommandHandler('activate', start.activate)
        ],
        states={
            "POST_AWATING": [
                MessageHandler(Filters.photo | Filters.video | Filters.voice |
                               Filters.audio | Filters.text & (~ Filters.command), start.post)
            ],
            "IN_GROUP": [
                MessageHandler(Filters.chat_type.supergroup, start.in_group)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.all, start.unsupported)
        ],
        name='main'
        # persistent=True
    )

    dispatcher.add_handler(main_conversation)

    updater.start_polling()
    updater.idle()
