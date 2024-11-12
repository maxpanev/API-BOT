import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import requests
from googletrans import Translator

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_number_fact(number):
    url = f"http://numbersapi.com/{number}/trivia"
    response = requests.get(url)
    if response.status_code == 200:
        translator = Translator()
        fact_in_english = response.text
        translation = translator.translate(fact_in_english, src='en', dest='ru')
        return translation.text
    else:
        return "Не удалось получить факт о числе. Попробуйте позже."

@dp.message(Command(commands=['fact']))
async def start(message: Message):
    await message.answer('Привет! Напишите мне любое число, и я расскажу вам интересный факт о нем.')

@dp.message()
async def send_number_fact(message: Message):
    try:
        number = int(message.text.strip())
        fact = get_number_fact(number)
        await message.answer(fact)
    except ValueError:
        await message.answer('Пожалуйста, введите корректное число.')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())