from pydub import AudioSegment
sound = AudioSegment.from_ogg("Путь")
sound.export("Путь.wav", format="wav")