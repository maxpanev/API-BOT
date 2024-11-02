import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN, API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start - для начала работы \n /help - для помощи \n /weather - для получения прогноза погоды')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я бот!')

async def fetch_weather():
    url = f'http://api.openweathermap.org/data/2.5/weather?q=Krasnodar&appid={API_KEY}&units=metric&lang=ru'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

@dp.message(Command('weather'))
async def weather(message: Message):
    weather_data = await fetch_weather()
    if weather_data:
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        await message.answer(f'Погода в Краснодаре: \nТемпература: {temp}°C\nОписание: {description}')
    else:
        await message.answer('Не удалось получить данные о погоде. Попробуйте позже.')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())