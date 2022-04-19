import os
from difflib import SequenceMatcher

import requests
import telebot
from telebot import types

from data import db_session
from data.songs import Song
from data.profile import User
from image_ot_qr import QR_Operation


db_session.global_init("db/musik.db")  # подключаем сессию sqlalchemy
URL = "https://api.telegram.org/bot"
__KEY__ = os.environ.get('APIKEY')
__KEY__ = "5381479308:AAF8YYIyWSYHDrvNkF34o-ZUByyAatL-EKI"  # это вообще левый бот для отладки
bot = telebot.TeleBot(__KEY__)
PAYMENTS_PROVIDER_TOKEN = os.environ.get('PAYKEY')
PAYMENTS_PROVIDER_TOKEN = "381764678:TEST:36167"

users_step = {}  # словарь статусов пользователей (некий аналог динамического json файла)

# кнопки
find_musick = types.KeyboardButton("Найти музыку")
add_musick = types.KeyboardButton("Добавить музыку")
other = types.KeyboardButton("Еще")
user = types.KeyboardButton("Профиль")
profile_change_photo = types.KeyboardButton("Сменить фон QR")
profile_change_gif = types.KeyboardButton("Сменить фон GIF")
profile_statistic = types.KeyboardButton("Статистика")
adv = types.KeyboardButton("Реклама")
text = types.KeyboardButton("Текст")
yes = types.KeyboardButton("Да")
back_button = types.KeyboardButton("Назад")
qr_button = types.KeyboardButton("QR код")

@bot.message_handler(content_types=["text",
                                    "start"])  # такая строка отвечает за тип обрабатывваемых соосбщений(эта за текст и команду старт)
def main(message):
    if not message.from_user.id in users_step:  # проверка на присутсвие в словаре
        users_step[message.from_user.id] = "home"

    if (message.text == "/start" or message.text == "Назад"):  # выход домой (если нажали старт или назад)

        users_step[message.from_user.id] = "home"  # меняем местонахождение пользователя в словаре

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # стиль кнопок
        markup.add(find_musick, add_musick, other)  # добавляем кнопки
        bot.send_message(message.chat.id,  # отправлем сообщение
                         text="Привет, {0.first_name}! Я тестируюсь".format(message.from_user), reply_markup=markup)
        # все последующие сточки делают тоже-самое, отличаясь кнопками и местоположением пользователя

    elif (message.text == "Еще"):

        users_step[message.from_user.id] = "other"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button, user, adv)
        bot.send_message(message.chat.id, text="Дополнительные функции", reply_markup=markup)

    elif (message.text == "Реклама"):
        users_step[message.from_user.id] = "schearch_for_adv"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id, text="Напишите название песни", reply_markup=markup)
        #musik_adv = types.LabeledPrice(label='Реклама песни', amount=10000)
        #if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            #bot.send_invoice(message.chat.id, title="Оплата", description="Реклама музыки {name} среди пользователей",
                             #provider_token=PAYMENTS_PROVIDER_TOKEN, currency="rub",
                             #is_flexible=False,
                             #prices=[musik_adv,],
                             #start_parameter='payment-test', invoice_payload="payload-test"
                             #)

    elif (message.text == "Профиль"):

        users_step[message.from_user.id] = "user"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(profile_change_photo, profile_change_gif, profile_statistic, back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Добро пожаловать в ваш профиль".format(
                             message.from_user), reply_markup=markup)

    elif (message.text == "Сменить фон QR"):
        users_step[message.from_user.id] = "profile_change_photo"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Скинь фотографию для фона QR".format(
                             message.from_user), reply_markup=markup)

    elif (message.text == "Сменить фон GIF"):
        users_step[message.from_user.id] = "profile_change_gif"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Скинь фотографию для фона GIF".format(
                             message.from_user), reply_markup=markup)

    elif (message.text == "Статистика"):
        users_step[message.from_user.id] = "profile_statistic"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Предоставляю вашу статистику:".format(
                             message.from_user), reply_markup=markup)
        bot.send_message(message.chat.id, text=f"Счёт прослушивания: {0}")
        bot.send_message(message.chat.id, text=f"Счёт добавления: {0}")
        bot.send_message(message.chat.id, text=f"Счёт рекламы: {0}")

    elif (message.text == "Добавить музыку"):

        users_step[message.from_user.id] = "musick_add"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Скинь сначала название, текст песни(можно часть, например только припев) затем фото и потом аудио в виде файла".format(
                             message.from_user), reply_markup=markup)

    elif (message.text == "Найти музыку"):

        users_step[message.from_user.id] = "musick_find"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(text)
        markup.row(back_button, qr_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Выбери формат поиска".format(message.from_user), reply_markup=markup)

    elif (message.text == "Текст"):

        users_step[message.from_user.id] = "text"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Напиши название или часть текста песни".format(
                             message.from_user),
                         reply_markup=markup)

    elif (message.text == "QR код"):

        users_step[message.from_user.id] = "qr"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, жду qr код".format(message.from_user),
                         reply_markup=markup)

    elif users_step[message.from_user.id] == "text":  # Запуск поиска по тексту
        send_message(message.chat.id, message.text, message)

    elif users_step[message.from_user.id] == "schearch_for_adv":  # Запуск поиска по тексту
        db_sess = db_session.create_session()
        result = list(db_sess.query(Song.gif, Song.song, Song.name).filter(Song.name == message.text).distinct())
        if result:
            users_step[message.from_user.id] = "check_for_adv"
            result = result[0]
            requests.get(f'{URL}{__KEY__}/sendPhoto?chat_id={message.chat.id}&photo={result[0]}&caption={result[2]}')
            requests.get(f"{URL}{__KEY__}/sendAudio?chat_id={message.chat.id}&audio={result[1]}")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(back_button, yes)
            bot.send_message(message.chat.id,
                             text="{0.first_name}, это то что нужно?".format(message.from_user),
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id,  # оно работает, осталось сделать поиск по таблице
                             text="Извините, ничего не нашлось".format(
                                 message.from_user))

    elif users_step[message.from_user.id] == "check_for_adv" and (message.text == "Да"):
        musik_adv = types.LabeledPrice(label='Реклама песни', amount=10000)
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            bot.send_invoice(message.chat.id, title="Оплата", description=f"Реклама среди пользователей",
            provider_token=PAYMENTS_PROVIDER_TOKEN, currency="rub",
            is_flexible=False,
            prices=[musik_adv,],
            start_parameter='payment-test', invoice_payload="payload-test"
            )


    elif users_step[message.from_user.id] == "musick_add":  # статус когда пользователь добавил название песни
        users_step[message.from_user.id] = ["musick_add-text", message.text]

    elif users_step[message.from_user.id][0] == "musick_add-text":  # статус когда пользователь добавил название песни
        users_step[message.from_user.id].append(message.text)
        users_step[message.from_user.id][0] = "musick_add-image"

    if users_step[message.from_user.id] == "profile_change_photo":  # статус когда пользователь добавил название песни
        users_step[message.from_user.id] = ["profile_change_photo"]

    elif users_step[message.from_user.id] == "profile_change_gif":  # статус когда пользователь добавил название песни
        users_step[message.from_user.id] = ["profile_change_gif"]

    print(users_step)

@bot.pre_checkout_query_handler(func=lambda query: True)  # функция проверки прихода оплаты
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])  # при успешной оплате
def payed(message):
    bot.send_message(message.chat.id, "Спасибо за покупку")
    # Нужно добавить рассылку рекламы


@bot.message_handler(content_types=['photo'])  # тут при отправке фото (не файл)
def image(message):
    if message.from_user.id in users_step:
        # проверка на нахождение в нужом шаге, иначе могут сломать отправив фото в неположеном месте
        if users_step[message.from_user.id][0] == "musick_add-image":
            file = message.photo[-1].file_id  # достаем id фото
            users_step[message.from_user.id].append(str(file))  # добавляем рядом с шагом
            users_step[message.from_user.id][0] = "musick_add-file"  # и ставим следющий шаг
        elif users_step[message.from_user.id] == "qr":  # тестовое условие декода qr
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = 'tmp/' + message.photo[1].file_id + ".png"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            dec = QR_Operation("tmp/" + message.photo[1].file_id)
            text_qr = dec.qr_decode()
            os.remove("tmp/" + message.photo[1].file_id + ".png")
            db_sess = db_session.create_session()
            if text_qr.isdigit():
                result = list(db_sess.query(Song.gif, Song.song, Song.name).filter(Song.id == int(text_qr)).distinct())
            else:
                result = False
            if result:
                result = result[0]
                requests.get(f'{URL}{__KEY__}/sendPhoto?chat_id={message.chat.id}&photo={result[0]}&caption={result[2]}')
                requests.get(f"{URL}{__KEY__}/sendAudio?chat_id={message.chat.id}&audio={result[1]}")
            else:
                bot.send_message(message.chat.id,  # оно работает, осталось сделать поиск по таблице
                             text="Извините, ничего не нашлось".format(
                                 message.from_user))
        elif users_step[message.from_user.id][0] == "profile_change_photo":
            file = message.photo[-1].file_id  # достаем id фото
            users_step[message.from_user.id].append(str(file))  # добавляем рядом с шагом
            users_step[message.from_user.id][0] = "profile_change_photo"  # и ставим следющий шаг
            #user = db_session.query(User).filter(User.user_id == message.from_user.id).first()
            #user.qr_back_image = file
            #db_session.commit()
            # затем записываем в таблицу профиля
            bot.send_message(message.chat.id, text="{0.first_name}, Фон успешно установлен".format(message.from_user))
        elif users_step[message.from_user.id][0] == "profile_change_gif":
            file = message.photo[-1].file_id  # достаем id фона gif
            users_step[message.from_user.id].append(str(file))  # добавляем рядом с шагом
            users_step[message.from_user.id][0] = "profile_change_photo"  # и ставим следющий шаг
            #user = db_session.query(User).filter(User.user_id == message.from_user.id).first()
            #user.qr_back_image = file
            #db_session.commit()
            bot.send_message(message.chat.id, text="{0.first_name}, Фон успешно установлен".format(message.from_user))


@bot.message_handler(content_types=['audio'])  # при отправке аудио (файл)
def doc(message):
    if message.from_user.id in users_step:
        if users_step[message.from_user.id][0] == "musick_add-file":
            file = str(message.audio.file_id)
            mus = Song()  # тут добавление в таблцу происходит
            mus.name = users_step[message.from_user.id][1]  # подробнее смотрите в файле с классом
            # Леня тут нужна гифка в blob
            mus.gif = users_step[message.from_user.id][3]
            mus.song = file
            mus.text = users_step[message.from_user.id][2]
            mus.id = message.from_user.id
            db_sess = db_session.create_session()  # собственно сессия
            db_sess.add(mus)  # вначале добавляем в сессию
            db_sess.commit()  # потом комитим обязательно
            bot.send_message(message.chat.id,
                             text="Успешно добавлено".format(
                                 message.from_user))


def send_message(chat_id, name, message):  # функция отправки нормального сообщения с песней
    db_sess = db_session.create_session()  # обязательно сессия для запросов
    result = list(db_sess.query(Song.gif, Song.song).filter(Song.name == name).distinct())  # запрос поиска по названи
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
        result = list(db_sess.query(Song.gif, Song.song, Song.name).filter(
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
