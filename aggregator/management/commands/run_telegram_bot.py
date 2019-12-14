import logging

from django.core.management import base
from django.conf import settings

import telebot

from aggregator.models import User, SearchWord


telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(token=settings.TOKEN)
bot.remove_webhook()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    User.objects.get_or_create(uid=message.chat.id)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Добавить слово')
    msg = bot.reply_to(message, 'Добро пожаловать!', reply_markup=markup)
    bot.register_next_step_handler(msg, process_word_step)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    send_welcome()


def process_word_step(message):
    msg = bot.reply_to(message, 'Введите слово для отслеживания:')
    bot.register_next_step_handler(msg, process_save_word_step)


def process_save_word_step(message):
    user, _ = User.objects.get_or_create(uid=message.chat.id)
    SearchWord.objects.create(user=user, word=message.text)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Добавить слово')
    msg = bot.reply_to(message, 'Спасибо, мы сохранили слово', reply_markup=markup)
    bot.register_next_step_handler(msg, process_save_word_step)


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.polling()
