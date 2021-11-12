import asyncio, msgpack, msgpack_numpy as m, elara
from aiogram import Bot, Dispatcher, executor
from func import *

API_TOKEN = '2041578738:AAGDx9CyqeQEoPnNcVlM0SlkFIlFvTphheM'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
uid = 490832297
db = elara.exe("encodings.db", True)


@dp.message_handler(lambda message: message.from_user.id == uid, commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Авторизація!")
    await asyncio.sleep(0.5)
    await message.answer("Авторизація успішна!", reply_markup=keyboard)


@dp.message_handler(lambda message: message.from_user.id == uid, text="●Очистити БД●")
async def db_reset(message: types.Message):
    db.set("seen encodings", msgpack.packb([face_recognition.face_encodings(face_recognition.load_image_file("./Faces/_test.jpg"))[0]], default=m.encode))
    db.commit()
    await message.answer("База даних була успішно очищена!", reply_markup=keyboard)


async def db_monitoring():
    while True:
        await asyncio.sleep(how_many_seconds_until_midnight())
        db.set('seen encodings', msgpack.packb([face_recognition.face_encodings(face_recognition.load_image_file("./Faces/_test.jpg"))[0]], default=m.encode))
        db.commit()
        await bot.send_message(uid, "Було проведено планову очистку бази даних!", disable_notification=True, reply_markup=keyboard)




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(db_monitoring())
    executor.start_polling(dp, skip_updates=True, timeout=None)
