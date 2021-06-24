#!/usr/bin/env python
# pylint: disable=C0116,W0613

from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          ConversationHandler)

#src import
import commands
from config import *

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), commands.gender)],
            PHOTO: [MessageHandler(Filters.photo, commands.photo), CommandHandler('skip', commands.skip_photo)],
            LOCATION: [
                MessageHandler(Filters.location, commands.location),
                CommandHandler('skip', commands.skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, commands.bio)],
        },
        fallbacks=[CommandHandler('cancel', commands.cancel)],
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