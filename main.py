import os
from difflib import SequenceMatcher

import requests
import telebot
from telebot import types

from Speech_rec import Recognition
from data import db_session
from data.songs import Song
from image_ot_qr import QR_Operation

with open("API_KEY", "r") as f:  # Считываем ключ
    __KEY__ = f.readline()

db_session.global_init("db/musik.db")  # подключаем сессию sqlalchemy
URL = "https://api.telegram.org/bot"
bot = telebot.TeleBot(__KEY__)

users_step = {}  # словарь статусов пользователей (некий аналог динамического json файла)

# кнопки
find_musick = types.KeyboardButton("Найти музыку")
add_musick = types.KeyboardButton("Добавить музыку")
speech = types.KeyboardButton("Голос")
text = types.KeyboardButton("Текст")
back_button = types.KeyboardButton("Назад")
qr_button = types.KeyboardButton("QR код")
rus = types.KeyboardButton("Русский")
eng = types.KeyboardButton("Английский")


@bot.message_handler(content_types=["text",
                                    "start"])  # такая строка отвечает за тип обрабатывваемых соосбщений(эта за текст и команду старт)
def main(message):
    if not message.from_user.id in users_step:  # проверка на присутсвие в словаре
        users_step[message.from_user.id] = "home"

    if (message.text == "/start" or message.text == "Назад"):  # выход домой (если нажали старт или назад)

        users_step[message.from_user.id] = "home"  # меняем местонахождение пользователя в словаре

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # стиль кнопок
        markup.add(find_musick, add_musick)  # добавляем кнопки
        bot.send_message(message.chat.id,  # отправлем сообщение
                         text="Привет, {0.first_name}! Я тестируюсь".format(message.from_user), reply_markup=markup)
        # все последующие сточки делают тоже-самое, отличаясь кнопками и местоположением пользователя

    elif (message.text == "Добавить музыку"):

        users_step[message.from_user.id] = "musick_add"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Скинь сначала название, затем фото потом аудио в виде файла".format(
                             message.from_user), reply_markup=markup)

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
        markup.add(back_button, rus, eng)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, выбери язык".format(message.from_user), reply_markup=markup)

    elif (message.text == "Русский") or (message.text == "Английский"):

        users_step[message.from_user.id] = message.text  # поступает Английский или Русский
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="Жду голосовую".format(message.from_user), reply_markup=markup)

    elif (message.text == "Текст"):

        users_step[message.from_user.id] = "text"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Напиши название или часть текста песни(пока только название)".format(
                             message.from_user),
                         reply_markup=markup)

    elif (message.text == "QR код"):

        users_step[message.from_user.id] = "qr"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, жду qr код".format(message.from_user),
                         reply_markup=markup)

    elif users_step[message.from_user.id] == "text":
        send_message(message.chat.id, message.text, message)

    elif users_step[message.from_user.id] == "musick_add":
        users_step[message.from_user.id] = ["musick_add-image", message.text]

    print(users_step)


@bot.message_handler(content_types=['photo'])  # тут при отправке фото (не файл)
def image(message):
    print(users_step, "image")
    if message.from_user.id in users_step:
        if users_step[message.from_user.id][
            0] == "musick_add-image":  # проверка на нахождение в нужом шаге, иначе могут сломать отправив фото в неположеном месте
            file = message.photo[-1].file_id  # достаем id фото
            users_step[message.from_user.id].append(str(file))  # добавляем рядом с шагом
            users_step[message.from_user.id][0] = "musick_add-file"  # и ставим следющий шаг
        elif users_step[message.from_user.id] == "qr":  # тестовое условие декода qr
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = 'nontime/' + message.photo[1].file_id + ".png"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            dec = QR_Operation("nontime/" + message.photo[1].file_id)
            text_qr = dec.qr_decode()
            os.remove("nontime/" + message.photo[1].file_id + ".png")
            # Сюда нужен поиск по id
            bot.send_message(message.chat.id,  # оно работает, осталось сделать поиск по таблице
                             text=text_qr.format(
                                 message.from_user))


@bot.message_handler(content_types=['audio'])  # при отправке аудио (файл)
def doc(message):
    print(users_step, "doc")
    if message.from_user.id in users_step:
        if users_step[message.from_user.id][0] == "musick_add-file":
            file = str(message.audio.file_id)
            mus = Song()  # тут добавление в таблцу происходит
            mus.name = users_step[message.from_user.id][1]  # подробнее смотрите в файле с классом
            mus.image = users_step[message.from_user.id][2]
            mus.song = file
            mus.text = "Саша по шоссе"  # замена тексту песни, нужна функция эмиля
            db_sess = db_session.create_session()  # собственно сессия
            db_sess.add(mus)  # вначале добавляем в сессию
            db_sess.commit()  # потом комитим обязательно
            bot.send_message(message.chat.id,
                             text="Успешно добавлено".format(
                                 message.from_user))


@bot.message_handler(content_types=['voice'])  # когда приходит голосовая
def voice(message):
    if users_step[message.from_user.id] == "Русский":
        to_speech("ru_RU", message)  # вынес отдельную функцию взаимодействия с классом Эмиля
    elif users_step[message.from_user.id] == "Английский":
        to_speech("eng_ENG", message)


def to_speech(lang, message):  # функия для взаимодействия с преобразованием в текст от Эмиля
    filename = str(message.from_user.id)  # название задается id пользователя (ну они же уникальные?)
    file_name_full = "nontime/" + filename + ".ogg"  # имя файла
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(
        file_info.file_path)  # скачали что-то, возможно бинарный. Леня твой выход, только не сломай
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)  # записываем что-то в файл(судя по всему бинарник)
    voicer = Recognition(file_name_full, lang)
    voicer = voicer.get_audio_messages()  # собственно колдуем из аудио текст
    send_message(message.chat.id, voicer, message)


def send_message(chat_id, name, message):  # функция отправки нормального сообщения с песней
    db_sess = db_session.create_session()  # обязательно сессия для запросов
    result = list(db_sess.query(Song.image, Song.song).filter(Song.name == name).distinct())  # запрос поиска по названи
    if result:  # если нашли имя
        result = result[0]  # тут был список с кортежем
        requests.get(f'{URL}{__KEY__}/sendPhoto?chat_id={chat_id}&photo={result[0]}&caption={name}')  # отправляем
        requests.get(f"{URL}{__KEY__}/sendAudio?chat_id={chat_id}&audio={result[1]}")  # ух-ты, тут тоже
    else:
        song = ["", 0]  # макс совпадение по умолчанию
        result = list(db_sess.query(Song.text).distinct())  # все тексты песен
        for i in result:
            i = i[0]
            s = SequenceMatcher(lambda x: x == " ", name, i)  # функция ищащая пересечения в проц. соотношении
            s = s.ratio()
            if s > song[1]:  # отбираем макс.
                song[1] = s
                song[0] = i
        print(song)
        result = list(db_sess.query(Song.image, Song.song, Song.name).filter(
            Song.text == song[0]).distinct())  # и ищем оставшееся по тексту
        if result:
            result = result[0]
            requests.get(
                f'{URL}{__KEY__}/sendPhoto?chat_id={chat_id}&photo={result[0]}&caption=Совпадение {round(song[1], 1) * 100}%, {result[2]}')
            requests.get(f"{URL}{__KEY__}/sendAudio?chat_id={chat_id}&audio={result[1]}")
        else:
            bot.send_message(message.chat.id,
                             text="Ничего не нашлось... Добавь эту песню нам в коллекцию".format(
                                 message.from_user))  # ну тут понятно по контексту, если ничего ненашли


def run():
    bot.polling(none_stop=True, interval=1)  # это запускает и обновляем бота


if __name__ == "__main__":
    run()
