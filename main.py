import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start - для начала работы \n /help - для помощи')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я бот!')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())