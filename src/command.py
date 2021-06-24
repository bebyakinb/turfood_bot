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
    hike_type_value = ''
    days_count = 0
    members_count = 0
    vegans_count = 0
    vegetarians_count = 0

    def __init__(self):
        # Enable logging

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def start(self, update: Update, context: CallbackContext) -> int:
        """Starts the conversation and asks the user about their hike type."""
        reply_keyboard = list(map(lambda el: [el], HIKE_TYPES))

        update.message.reply_text(
            'Давай составим раскладку для твоего похода.'
            'Для начала ответь на несколько вопросов.\n\n'
            'Какой тип похода ты планируешь?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return HIKE_TYPE

    def hike_type(self, update: Update, context: CallbackContext) -> int:
        """Stores the hike type and asks for a days."""
        user = update.message.from_user
        self.hike_type_value = update.message.text
        # self.logger.info("HikeType of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'Круто, теперь укажи количество дней',
            reply_markup=ReplyKeyboardRemove()
        )

        return DAYS

    def days(self, update: Update, context: CallbackContext) -> int:
        """Stores the days and asks for a members."""
        user = update.message.from_user
        self.days_count = int(update.message.text)
        # self.logger.info("HikeType of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'Отлично, теперь укажи количество участников'
        )

        return MEMBERS

    def members(self, update: Update, context: CallbackContext) -> int:
        """Stores number of members and asks for number of vegans."""
        user = update.message.from_user
        self.members_count = int(update.message.text)
        # self.logger.info("Members of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'Окей, а сколько из них веганы(не едят мясо, рыбо, молочку, яица)?'
        )

        return VEGANS

    def vegans(self, update: Update, context: CallbackContext) -> int:
        """Stores the number of vegans and asks for number of vegetarians."""
        user = update.message.from_user
        self.vegans_count = int(update.message.text)
        # self.logger.info("Members of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'А помимо веганов есть такие, кто просто не ест мясо и рыбу?'
        )

        return VEGETARIANS

    def vegetarians(self, update: Update, context: CallbackContext) -> int:
        """Stores the number of vegetarians and return total."""
        user = update.message.from_user
        self.vegetarians_count = int(update.message.text)
        # self.logger.info("Members of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'Итог.\n'
            'Тип похода : ' + self.hike_type_value + '\n'
            'Кол-во дней : ' + str(self.days_count) + '\n'
            'Кол-во учстников : ' + str(self.members_count) + '\n'
            '   веганов : ' + str(self.vegans_count) + '\n'
            '   вегетарианцев : ' + str(self.vegetarians_count) + '\n'
            '   остальных : ' + str(self.members_count - self.vegetarians_count - self.vegans_count)
        )

        return ConversationHandler.END

    def cancel(self, update: Update, context: CallbackContext) -> int:
        """Cancels and ends the conversation."""
        user = update.message.from_user
        self.logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text(
            'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END
