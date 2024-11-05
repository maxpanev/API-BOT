# Подключаем библиотеки и токены
import asyncio
import aiohttp
import random
import os
from gtts import gTTS
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from googletrans import Translator

from config import TOKEN, API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

# Отправляем фото боту в Telegram, он сохраняет фото в файл img
@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Ого, какая фотка!', 'Прикольное фото)', 'Мне нужны фотографии Человека-Паука!!!']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')

# Подключаем функцию help
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start - для начала работы \n /help - для помощи \n /weather - для получения прогноза погоды \n /training - для получения новой тренировки')

# Подключаем функцию start

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}') # бот будет обращаться к пользователю по имени

# Подключаем сайт OpenWeatherMap который показывает погоду на текущий день
async def fetch_weather():
    url = f'http://api.openweathermap.org/data/2.5/weather?q=Krasnodar&appid={API_KEY}&units=metric&lang=ru'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Подключаем функцию weather для вывода информации о погоде

@dp.message(Command('weather'))
async def weather(message: Message):
    weather_data = await fetch_weather()
    if weather_data:
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        await message.answer(f'Погода в Краснодаре: \nТемпература: {temp}°C\nОписание: {description}')
    else:
        await message.answer('Не удалось получить данные о погоде. Попробуйте позже.')

# Подключаем функцию training для получения тренировки в текстовом и голосовом сообщении
@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Грудь + Трицепс:\n1. Жим лежа: 3 подхода по 15 повторений\n2. Разгибание рук с гантелями в наклоне: 3 подхода по 20 повторений\n3. Планка: 3 подхода по 30 секунд",
       "Спина + Бицепс:\n1. Мертвая тяга: 3 подхода по 15 повторений\n2. Подъем штанги на бицепс: 3 подхода по 20 повторений\n3. Подьемы ног на пресс: 3 подхода по 20 раз",
       "Ноги + Плечи:\n1. Приседания со штангой: 3 подхода по 15 повторений\n2. Жим Арнольда: 3 подхода по 20 повторений\n3. Подъемы на икры с гантелями: 3 подхода по 30 раз"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

   tts = gTTS(text=rand_tr, lang='ru')
   tts.save('training.ogg')
   audio = FSInputFile('training.ogg')
   await bot.send_voice(message.chat.id, audio)
   os.remove('training.ogg')

# Переводим текст сообщения с русского на английский
@dp.message()
async def start(message: types.Message):
    translated = translator.translate(message.text, src='ru', dest='en')
    await message.answer(translated.text)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())