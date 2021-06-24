#!/usr/bin/env python
# pylint: disable=C0116,W0613

from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          ConversationHandler, )

# src import
from command import Command
from config import *


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)
    command = Command()
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', command.start)],
        states={
            HIKE_TYPE: [MessageHandler(Filters.regex(r'^(' + '|'.join(map(str, HIKE_TYPES)) + ')$'), command.hike_type)],
            DAYS: [MessageHandler(Filters.regex(r'^\d+$'), command.days)],
            MEMBERS: [MessageHandler(Filters.regex(r'^\d+$'), command.members)],
            VEGANS: [MessageHandler(Filters.regex(r'^\d+$'), command.vegans)],
            VEGETARIANS: [MessageHandler(Filters.regex(r'^\d+$'), command.vegetarians)],
        },
        fallbacks=[CommandHandler('cancel', command.cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
