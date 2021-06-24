#!/usr/bin/env python

import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove)
from telegram.ext import (
    CallbackContext,
    ConversationHandler)

from config import *


class Command:
    # Enable logging
    def __init__(self):         
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def start(self, update: Update, context: CallbackContext) -> int:
        """Starts the conversation and asks the user about their gender."""
        reply_keyboard = [['Boy', 'Girl', 'Other']]

        update.message.reply_text(
            'Hi! My name is Professor Bot. I will hold a conversation with you. '
            'Send /cancel to stop talking to me.\n\n'
            'Are you a boy or a girl?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return GENDER

    def gender(self, update: Update, context: CallbackContext) -> int:
        """Stores the selected gender and asks for a photo."""
        user = update.message.from_user
        self.logger.info("Gender of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'I see! Please send me a photo of yourself, '
            'so I know what you look like, or send /skip if you don\'t want to.',
            reply_markup=ReplyKeyboardRemove(),
        )

        return PHOTO

    def photo(self, update: Update, context: CallbackContext) -> int:
        """Stores the photo and asks for a location."""
        user = update.message.from_user
        photo_file = update.message.photo[-1].get_file()
        photo_file.download('user_photo.jpg')
        self.logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
        update.message.reply_text(
            'Gorgeous! Now, send me your location please, or send /skip if you don\'t want to.'
        )

        return LOCATION

    def skip_photo(self, update: Update, context: CallbackContext) -> int:
        """Skips the photo and asks for a location."""
        user = update.message.from_user
        self.logger.info("User %s did not send a photo.", user.first_name)
        update.message.reply_text(
            'I bet you look great! Now, send me your location please, or send /skip.'
        )

        return LOCATION

    def location(self, update: Update, context: CallbackContext) -> int:
        """Stores the location and asks for some info about the user."""
        user = update.message.from_user
        user_location = update.message.location
        self.logger.info(
            "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
        )
        update.message.reply_text(
            'Maybe I can visit you sometime! At last, tell me something about yourself.'
        )

        return BIO

    def skip_location(self, update: Update, context: CallbackContext) -> int:
        """Skips the location and asks for info about the user."""
        user = update.message.from_user
        self.logger.info("User %s did not send a location.", user.first_name)
        update.message.reply_text(
            'You seem a bit paranoid! At last, tell me something about yourself.'
        )

        return BIO

    def bio(self, update: Update, context: CallbackContext) -> int:
        """Stores the info about the user and ends the conversation."""
        user = update.message.from_user
        self.logger.info("Bio of %s: %s", user.first_name, update.message.text)
        update.message.reply_text('Thank you! I hope we can talk again some day.')

        return ConversationHandler.END

    def cancel(self, update: Update, context: CallbackContext) -> int:
        """Cancels and ends the conversation."""
        user = update.message.from_user
        self.logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text(
            'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END
