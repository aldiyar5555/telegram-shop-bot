from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = "8709196130:AAHqY0tUxruSWSE34zHGp015oVUnqejX99M"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

admin_id = 123456789

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Купить товар", callback_data="buy"))

    await message.answer("Добро пожаловать в магазин!", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "buy")
async def buy(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите количество товара")

@dp.message_handler()
async def order(message: types.Message):

    text = f"""
Новый заказ
User: {message.from_user.username}
Количество: {message.text}
"""

    await bot.send_message(admin_id, text)

    await message.answer("Заказ отправлен!")

if __name__ == "__main__":
    executor.start_polling(dp)