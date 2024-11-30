from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_R = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb_R.add(button, button2)
kb_R.add(button3)

kb_I = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_I.add(button, button2)

kb_IP = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='centrum', callback_data="product_buying")],
        [InlineKeyboardButton(text='compvitB', callback_data="product_buying")],
        [InlineKeyboardButton(text='vitD3', callback_data="product_buying")],
        [InlineKeyboardButton(text='vitB', callback_data="product_buying")]
    ]
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

products = get_all_products()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выберите опцию", reply_markup=kb_I)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await  UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    bmr = 10 * int(data.get('age', 0)) + 6.25 * int(data.get('growth', 0)) - 5 * int(data.get('weight', 0)) + 5
    await message.answer(f"{bmr}")
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    print("Привет! Я бот помогающий твоему здоровью.")
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb_R)


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    for product in products:
        image_path = f'files/{product["title"].lower().replace(" ", "_")}.jpg'
        with open(image_path, "rb") as image_file:
            await message.answer_photo(
                image_file,
                caption=f"Название: {product['title']} | "
                        f"Описание: {product['description']} | "
                        f"Цена: {product['price']}"
            )
    await message.answer("Выберите продукт для покупки:", reply_markup=kb_IP)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler()
async def all_massages(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
