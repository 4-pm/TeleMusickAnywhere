import telebot
from telebot import types

with open("API_KEY", "r") as f:
    __KEY__ = f.readline()

bot = telebot.TeleBot(__KEY__)

users_step = {}

find_musick = types.KeyboardButton("Найти музыку")
add_musick = types.KeyboardButton("Добавить музыку")
speech = types.KeyboardButton("Голос")
text = types.KeyboardButton("Текст")
back_button = types.KeyboardButton("Назад")
qr_button = types.KeyboardButton("QR код")

@bot.message_handler(content_types=['text', "start"])
def main(message):

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
        print(users_step)

    elif (message.text == "Голос"):

        users_step[message.from_user.id] = "voice"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, жду голосовой".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def image(message):
    print("get")
    if users_step[message.from_user.id] == "musick_find":
        file = message.photo[-1].file_id
        print(file)
        #bot.send_message(message.chat.id, te)


bot.polling(none_stop=True, interval=1)