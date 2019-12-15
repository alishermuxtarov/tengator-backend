import logging

from django.core.management import base
from django.conf import settings

import telebot
from telebot.apihelper import ApiException

from aggregator.models import User, SearchWord


telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(token=settings.TOKEN)
try:
    bot.remove_webhook()
except ApiException:
    pass


def default_keyboard(obj, msg, reply=True):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Добавить слово')
    if reply is True:
        return bot.reply_to(obj, msg, reply_markup=markup)
    return bot.send_message(obj.chat.id, msg, reply_markup=markup)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    user, created = User.objects.get_or_create(uid=message.chat.id)
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = telebot.types.KeyboardButton(text="Отправить номер", request_contact=True)
    keyboard.add(reg_button)
    msg = bot.send_message(
        message.chat.id,
        "Добро пожаловать!\nДля регистрации, необходимо ввести или отправить номер телефона",
        reply_markup=keyboard)
    bot.register_next_step_handler(msg, process_registration)


def process_registration(message):
    msg = bot.send_message(message.chat.id, "Введите код с СМС")
    bot.register_next_step_handler(msg, process_sms)


def process_sms(message):
    msg = default_keyboard(message, 'Спасибо. Проверка прошла успешно.')
    bot.register_next_step_handler(msg, process_word_step)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    msg = default_keyboard(message, 'Неизвестная команда!')
    bot.register_next_step_handler(msg, process_word_step)


def process_word_step(message):
    msg = bot.reply_to(message, 'Введите слово для отслеживания:')
    bot.register_next_step_handler(msg, process_save_word_step)


def process_save_word_step(message):
    user, _ = User.objects.get_or_create(uid=message.chat.id)
    if SearchWord.objects.filter(user=user, word=message.text).exists():
        msg = bot.send_message(message.chat.id, "Данное слово уже добавлено!")
        return bot.register_next_step_handler(msg, process_save_word_step)

    SearchWord.objects.create(user=user, word=message.text)

    msg = default_keyboard(message, 'Спасибо, мы сохранили слово')
    bot.register_next_step_handler(msg, process_word_step)


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.polling()
