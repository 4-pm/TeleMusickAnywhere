import speech_recognition as speech_recog


sample_audio = speech_recog.AudioFile('E:/Telegram_voice_bot/test.wav')  # открытие файла с речью

recog = speech_recog.Recognizer()

with sample_audio as audio_file:
    audio_content = recog.record(audio_file)

print(recog.recognize_google(audio_content, language="en-EN"))  # распознавание речи
