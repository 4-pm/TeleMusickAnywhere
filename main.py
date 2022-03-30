import telebot
from telebot import types

with open("API_KEY", "r") as f:
    __KEY__ = f.readline()

bot = telebot.TeleBot(__KEY__)
#VOICE = False

@bot.message_handler(content_types=['text'])
def main(message):

    if (message.text == "/start" or message.text == "Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Найти музыку")
        markup.add(btn1)
        bot.send_message(message.chat.id,
                         text="Привет, {0.first_name}! Я тестируюсь".format(message.from_user), reply_markup=markup)

    elif (message.text == "Найти музыку"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton("Назад")
        btn1 = types.KeyboardButton("Голос")
        btn2 = types.KeyboardButton("Текст")
        markup.add(back_button, btn1, btn2)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, Выбери формат поиска".format(message.from_user), reply_markup=markup)

    elif (message.text == "Голос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton("Назад")
        markup.add(back_button)
        bot.send_message(message.chat.id,
                         text="{0.first_name}, жду голосовой".format(message.from_user), reply_markup=markup)
        # Место


bot.polling(none_stop=True, interval=0)