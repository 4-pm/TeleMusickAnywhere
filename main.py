import telebot
import requests
import sqlite3
from difflib import SequenceMatcher
from telebot import types

with open("API_KEY", "r") as f:
    __KEY__ = f.readline()

URL = "https://api.telegram.org/bot"
bot = telebot.TeleBot(__KEY__)
con = sqlite3.connect("db/music.db", check_same_thread=False)
cur = con.cursor()

users_step = {}

find_musick = types.KeyboardButton("Найти музыку")
add_musick = types.KeyboardButton("Добавить музыку")
speech = types.KeyboardButton("Голос")
text = types.KeyboardButton("Текст")
back_button = types.KeyboardButton("Назад")
qr_button = types.KeyboardButton("QR код")

@bot.message_handler(content_types=["text", "start"])
def main(message):

    if not message.from_user.id in users_step:
        users_step[message.from_user.id] = "home"

    if (message.text == "/start" or message.text == "Назад"):

        users_step[message.from_user.id] = "home"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(find_musick, add_musick)
        bot.send_message(message.chat.id,
                         text="Привет, {0.first_name}! Я тестируюсь".format(message.from_user), reply_markup=markup)

    elif (message.text == "Добавить музыку"):

        users_step[message.from_user.id] = "musick_add"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Скинь сначала название, затем фото потом аудио в виде файла".format(message.from_user), reply_markup=markup)

    elif (message.text == "Найти музыку"):

        users_step[message.from_user.id] = "musick_find"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(speech, text)
        markup.row(back_button, qr_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Выбери формат поиска".format(message.from_user), reply_markup=markup)

    elif (message.text == "Голос"):

        users_step[message.from_user.id] = "voice"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, жду голосовой".format(message.from_user), reply_markup=markup)

    elif (message.text == "Текст"):

        users_step[message.from_user.id] = "text"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Напиши название или часть текста песни(пока только название)".format(message.from_user),
                         reply_markup=markup)

    elif users_step[message.from_user.id] == "text":
        send_mesage(message.chat.id, message.text, message)

    elif users_step[message.from_user.id] == "musick_add":
        users_step[message.from_user.id] = ["musick_add-image", message.text]

    print(users_step)






@bot.message_handler(content_types=['photo'])
def image(message):
    print(users_step, "image")
    if message.from_user.id in users_step:
        if users_step[message.from_user.id][0] == "musick_add-image":
            file = message.photo[-1].file_id
            users_step[message.from_user.id].append(str(file))
            users_step[message.from_user.id][0] = "musick_add-file"

@bot.message_handler(content_types=['audio'])
def doc(message):
    print(users_step, "doc")
    if message.from_user.id in users_step:
        if users_step[message.from_user.id][0] == "musick_add-file":
            file = str(message.audio.file_id)
            cur.execute(f"""INSERT INTO songs VALUES('{users_step[message.from_user.id][2]}',
                        '{users_step[message.from_user.id][1]}',
                        '{file}', 'No text')""")
            con.commit()
            print("ok")


def send_mesage(chat_id, name, message):
    result = cur.execute(f"""SELECT qr, song FROM songs
                            WHERE name = '{name}'""").fetchall()
    if result:
        result = result[0]
        requests.get(f'{URL}{__KEY__}/sendPhoto?chat_id={chat_id}&photo={result[0]}&caption={name}')
        requests.get(f"{URL}{__KEY__}/sendAudio?chat_id={chat_id}&audio={result[1]}")
    else:
        song = ["", 0]
        result = cur.execute(f"""SELECT text FROM songs""").fetchall()
        print(result)
        for i in result:
            i = i[0]
            s = SequenceMatcher(lambda x: x == " ", name, i)
            s = s.ratio()
            if s > song[1]:
                song[1] = s
                song[0] = i
        print(song)
        result = cur.execute(f"""SELECT qr, song, name FROM songs
                                    WHERE text = '{song[0]}'""").fetchall()
        if result:
            result = result[0]
            requests.get(f'{URL}{__KEY__}/sendPhoto?chat_id={chat_id}&photo={result[0]}&caption=Совпадение {round(song[1], 1) * 100}%, {result[2]}')
            requests.get(f"{URL}{__KEY__}/sendAudio?chat_id={chat_id}&audio={result[1]}")
        else:
            bot.send_message(message.chat.id,
                             text="Ничего не нашел(... Добавь эту песню нам в коллекцию".format(
                                 message.from_user))


bot.polling(none_stop=True, interval=1)