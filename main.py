from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = "YOUR_TOKEN"
admin_id = 123456789  # Твой телеграм ID

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class OrderState(StatesGroup):
    waiting_for_quantity = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Купить товар", callback_data="buy"))
    await message.answer("Добро пожаловать в магазин!", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "buy")
async def buy(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите количество товара")
    await OrderState.waiting_for_quantity.set()

@dp.message_handler(state=OrderState.waiting_for_quantity)
async def order(message: types.Message, state: FSMContext):
    text = f"""
Новый заказ
User: @{message.from_user.username}
Количество: {message.text}
"""
    await bot.send_message(admin_id, text)
    await message.answer("Заказ отправлен!")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp)