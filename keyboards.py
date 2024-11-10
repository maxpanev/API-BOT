from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", url="https://ura.news/news/1052841392")],
    [InlineKeyboardButton(text="Музыка", url="https://zvuk.com/track/124206497")],
    [InlineKeyboardButton(text="Видео", url="https://rutube.ru/video/23f1e56c3f1f7dce713114567dd84019/")]
])

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data='dynamic')]
])

text1 = "Это текст для опции 1"
text2 = "Это текст для опции 2"
test = [("Опция 1", text1), ("Опция 2", text2)]

async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key, callback_data in test:
        keyboard.add(InlineKeyboardButton(text=key, callback_data=callback_data))
    return keyboard.adjust(2).as_markup()