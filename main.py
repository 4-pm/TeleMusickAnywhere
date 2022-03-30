import telebot

with open("API_KEY", "r") as f:
    __KEY__ = f.readline()

bot = telebot.TeleBot(__KEY__)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, message)


bot.polling(none_stop=True, interval=0)