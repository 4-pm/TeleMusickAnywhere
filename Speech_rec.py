import os
import speech_recognition as sr
import subprocess
import datetime


class recognition:
    def __init__(self, file_name):
        self.file_name = file_name
        self.logfile = 'logs/' + str(datetime.date.today()) + '.log'

    def audio_to_text(self, name: str):
        r = sr.Recognizer()
        message = sr.AudioFile(name)
        with message as source:
            audio = r.record(source)
        result = r.recognize_google(audio, language="ru_RU")
        return result

    def get_audio_messages(self, message):
        try:
            directory = os.getcwd()
            subprocess.call(
                f'{directory}/bin/ffmpeg.exe -i {directory}/{self.file_name} {directory}/{self.file_name[:-4]}.wav')
            result = self.audio_to_text(self.file_name[:-4] + '.wav')
            return result

        except sr.UnknownValueError:
            with open(self.logfile, 'a', encoding='utf-8') as file:
                file.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' +
                           str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' +
                           str(message.from_user.username) + ':' + str(
                    message.from_user.language_code) + ':Message is empty.\n')
            return -1

        except Exception as e:
            with open(self.logfile, 'a', encoding='utf-8') as file:
                file.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' +
                           str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' +
                           str(message.from_user.username) + ':' + str(message.from_user.language_code) + ':' + str(
                    e) + '\n')
            return -2

        finally:
            pass
            os.remove(self.file_name[:-4] + '.wav')
            os.remove(self.file_name)
