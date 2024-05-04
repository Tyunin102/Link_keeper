import re
import telebot
import sqlite3


bot = telebot.TeleBot('6487431060:AAGNy4HbC7B1uzlX6XtiXo_gn9rbEPsmNMM')

with sqlite3.connect('links.db') as db:
    db.execute('''CREATE TABLE IF NOT EXISTS links
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id TEXT, link TEXT)''')
    db.commit()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я бот, который поможет \nне\
забыть прочитать статьи, найденные \nтобой в интернете :)\n- Чтобы я запомнил твою статью, \nдостаточно передать \
мне ссылку \nна нее. К примеру https://example.com\n- Чтобы получить случайную \nстатью, достаточно передать мне \n\
команду /get_article \nНо помни! Отдавая статью тебе на \nпрочтение, она больше не \nхранится в моей базе. Так что \
тебе\nточно нужно ее изучить', parse_mode='html')


@bot.message_handler(commands=['get_article'])
def get_article(message):
    with sqlite3.connect('links.db') as db:
        cursor = db.execute("SELECT link FROM links WHERE chat_id = ? ORDER BY RANDOM() LIMIT 1", (message.chat.id,))
        result = cursor.fetchone()
        if result:
            bot.send_message(message.chat.id, f'Вот ваша статья: {result[0]}')
            db.execute("DELETE FROM links WHERE link = ? AND chat_id = ?", (result[0], message.chat.id))
            db.commit()
        else:
            bot.send_message(message.chat.id, 'Вы пока не сохранили ни одну ссылку\nCамое время начать!')


@bot.message_handler()
def save_article(message):
    with sqlite3.connect('links.db') as db:
        links = re.findall("(?P<url>https?://[^\s]+)", message.text.strip().lower())
        if not links:
            bot.send_message(message.chat.id, 'Не смог найти ссылку в вашем сообщении :(\n'
                                              'Пример ссылки: https://example.com', parse_mode='html')
        else:
            for link in links:
                db.execute("INSERT INTO links (chat_id, link) VALUES (?, ?)", (message.chat.id, link))
            db.commit()
            links_to_save = "\n- ".join(links)
            bot.send_message(message.chat.id, 'Сохранил!\n- ' + links_to_save, parse_mode='html')


bot.polling(none_stop=True)
