import re
import telebot
import sqlite3

from config import API_token
from db_query import CREATE_TABLE, SELECT_LINK, DELETE_LINK, INSERT_LINK
from messages_text import START_MESSAGE, EMPTY_DB, GET_SAVED_LINK, BAD_USER_ENTER, SUCCESSFUL_SAVE, HELP_MESSAGE


bot = telebot.TeleBot(API_token)

with sqlite3.connect('links.db') as db:
    db.execute(CREATE_TABLE)
    db.commit()


@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(
        message.chat.id,
        START_MESSAGE.format(message.from_user.first_name),
        parse_mode='html'
    )


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(
        message.chat.id,
        HELP_MESSAGE.format(message.from_user.first_name),
        parse_mode='html'
    )


@bot.message_handler(commands=['get_article'])
def get_article(message):
    with sqlite3.connect('links.db') as db:
        cursor = db.execute(SELECT_LINK, (message.chat.id,))
        result = cursor.fetchone()
        if result:
            bot.send_message(message.chat.id, GET_SAVED_LINK.format(result[0]))
            db.execute(DELETE_LINK, (result[0], message.chat.id))
            db.commit()
        else:
            bot.send_message(message.chat.id, EMPTY_DB)


@bot.message_handler()
def save_article(message):
    with sqlite3.connect('links.db') as db:
        links = re.findall("(?P<url>https?://[^\s]+)", message.text.strip().lower())
        if not links:
            bot.send_message(message.chat.id, BAD_USER_ENTER, parse_mode='html')
        else:
            for link in links:
                db.execute(INSERT_LINK, (message.chat.id, link))
            db.commit()
            links_to_save = "\n- ".join(links)
            bot.send_message(message.chat.id, SUCCESSFUL_SAVE + links_to_save, parse_mode='html')


bot.polling(none_stop=True)
