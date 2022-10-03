import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Объект бота
bot = Bot(token="")
# Диспетчер для бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def cmd_start(message:types.message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('/download')
    keyboard.add(button1)
    await message.answer('Привет, я такой то такой делаю вот то.', reply_markup=keyboard)

@dp.message_handler(commands="download")
async def cmd_download(message:types.message):
    await message.answer('')