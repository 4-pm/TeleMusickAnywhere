import os
import telebot
import requests
import speech_recognition as sr
import subprocess
import datetime


with open("API_KEY", "r") as f:
    __KEY__ = f.readline()

bot = telebot.TeleBot(__KEY__)

logfile = 'logs/' + str(datetime.date.today()) + '.log'


def audio_to_text(dest_name: str):
    r = sr.Recognizer()
    message = sr.AudioFile(dest_name)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language="ru_RU")
    return result


@bot.message_handler(content_types=['voice'])
def get_audio_messages(message):
    try:
        print("Started recognition...")
        #  это скачивание
        #  начало
        file_info = bot.get_file(message.voice.file_id)
        path = file_info.file_path
        file_name = os.path.basename(path)  # имя файла

        doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(__KEY__, file_info.file_path))
        with open(file_name, 'wb') as file:
            file.write(doc.content)
        #  конец
        directory = os.getcwd()
        subprocess.call(
            f'{directory}/bin/ffmpeg.exe -i {directory}/{file_name} {directory}/{file_name[:-4]}.wav')
        result = audio_to_text(file_name[:-4] + '.wav')
        print(2)
        bot.send_message(message.from_user.id, format(result))

    except sr.UnknownValueError:
        bot.send_message(message.from_user.id, "Прошу прощения, но я не разобрал сообщение, или оно поустое...")
        with open(logfile, 'a', encoding='utf-8') as file:
            file.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' +
                       str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' +
                       str(message.from_user.username) + ':' + str(
                message.from_user.language_code) + ':Message is empty.\n')

    except Exception as e:
        bot.send_message(message.from_user.id,
                         "Что-то пошло не так, но наши смелые инженеры уже трудятся над решением... \n"
                         "Да ладно, никто эту ошибку исправлять не будет, она просто потеряется в логах.")
        with open(logfile, 'a', encoding='utf-8') as file:
            file.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' +
                       str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' +
                       str(message.from_user.username) + ':' + str(message.from_user.language_code) + ':' + str(
                e) + '\n')

    finally:
        pass
        os.remove(file_name[:-4] + '.wav')
        os.remove(file_name)


bot.polling(none_stop=True, interval=0)
