from aiohttp import web
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

TOKEN = "8800078553:AAE6a3zHomzDN6ANcMWU59JCdiy0FOA7EQs"
bot = Bot(token=TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    name = State()
    phone_number = State()
    object_type = State()
    price = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "Привет! Я бот-агент по недвижимости. Чтобы начать, введите ваше имя."
    )
    await state.set_state(Form.name)


@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введите ваш номер телефона.")
    await state.set_state(Form.phone_number)


@dp.message(Form.phone_number)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer(
        "Какой объект вас интересует? (например, квартира, дом)"
    )
    await state.set_state(Form.object_type)


@dp.message(Form.object_type)
async def process_object_type(message: types.Message, state: FSMContext):
    await state.update_data(object_type=message.text)
    await message.answer("Укажите желаемый бюджет.")
    await state.set_state(Form.price)


@dp.message(Form.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await message.answer(
        f"Спасибо! Данные приняты:\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone_number']}\n"
        f"Объект: {data['object_type']}\n"
        f"Бюджет: {data['price']}"
    )
    await state.clear()



async def main():
    await dp.start_polling(bot)


async def handle(request):
    return web.Response(text="Bot is running")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
async def main_with_server():
    await start_web_server()
    await main()

if __name__ == "__main__":
    asyncio.run(main_with_server())
    
