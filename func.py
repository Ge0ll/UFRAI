import os, face_recognition
from aiogram import types
from datetime import datetime, timedelta


known_face_encodings = []
known_face_names = []

for file in os.listdir("./Faces"):
    if file.endswith(".jpg"):
        known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file("./Faces/"+file))[0])
        known_face_names.append(file.rpartition(".")[0])

key = types.reply_keyboard.KeyboardButton("●Очистити БД●")
keyboard = types.reply_keyboard.ReplyKeyboardMarkup([[key]], True, False)

def how_many_seconds_until_midnight():
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month,
                        day=tomorrow.day, hour=0, minute=0, second=0)
    return (midnight - datetime.now()).seconds
