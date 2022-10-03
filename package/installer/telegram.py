import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from createdb import create_connection, return_path_db, return_users, return_bot_password, return_bot_token, execute_query
from createdirectory import Directory
import pathlib
from shutil import make_archive
from os import remove

# Объект бота
bot = Bot(token=f"5559131940:AAHCEeYtb9gmVE88BFm8qOQpcrSVTSZvMkg") # return_bot_token
# Диспетчер для бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

path = return_path_db(create_connection())[0]
users = return_users(create_connection())[0]
bot_pass = return_bot_password(create_connection())[0]

PC = Directory()

class Form(StatesGroup):
    msg_dir = State()
    msg_ans = State()
    msg_lf = State()

@dp.message_handler(commands='start')
async def start(messages:types.Message, state: FSMContext):
    if messages.chat.username in users:
        await menu(message=messages, state=state)
    else:
        await messages.answer('Пожалустай введите пароль от бота.')
        await Form.msg_lf.set()

@dp.message_handler(state=Form.msg_lf)
async def auth(message: types.Message, state: FSMContext):
    await state.update_data(msg_lf = message.text)
    data = await state.get_data()
    if data['msg_lf'] == '1111': # Нужно вернуть пароль с дб
        execute_query(create_connection(),f"""
        INSERT INTO
          users_names(name)
        VALUES
          ('{message.chat.username}')
        """)
        await message.answer('Пароль подтвержден. Вы в вайт-листе')
        await menu(message=message, state=state)
    else:
        await message.answer('Пароль не подтвержден. Попробуйте еще раз.')
        await start(messages=message, state=state)

async def menu(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if PC.return_files() == []:
        await message.answer('У Вас нет файлов/папок')
        keyboard.add(types.KeyboardButton('Да'))
        keyboard.add(types.KeyboardButton('Нет'))
        await message.answer('Хотите загрузить файл?', reply_markup=keyboard)
        await Form.msg_dir.set()
    else:
        for file in PC.return_files():
            keyboard.add(types.KeyboardButton(str(file)))
        await message.answer('Пожалуйста выберите файл/папку.', reply_markup=keyboard)
        await Form.msg_dir.set()

@dp.message_handler(state=Form.msg_dir)
async def selector(message: types.Message, state: FSMContext):
    await state.update_data(msg_dir = message.text, msg_lf = 1)
    data = await state.get_data()
    if data['msg_dir'] == 'Вернуться домой':
        PC.return_home()
        await state.update_data(msg_dir = PC.path)
        await menu(message=message, state=state)
    else:
        PC.choose_fileordir(str(data['msg_dir']).split('/' or '\\')[-1])
        # print(str(data['msg_dir']).split('/' or '\\')[-1])
        if PC.is_dir() == True:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton('Скачать всю папку'))
            keyboard.add(types.KeyboardButton('Выбрать файл'))
            keyboard.add(types.KeyboardButton('Загрузить файл в папку'))
            keyboard.add(types.KeyboardButton('Вернуться домой'))
            await message.answer('Это папка, выберите что хотите сделать.', reply_markup=keyboard)
            await Form.msg_ans.set()
        elif PC.is_dir() == False:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton('Скачать файл'))
            keyboard.add(types.KeyboardButton('Вернуться домой'))
            await message.answer('Это файл, выберите что хотите сделать', reply_markup=keyboard)
            await Form.msg_ans.set()

@dp.message_handler(state=Form.msg_ans, content_types=['text','photo', 'document'])
async def answer(message: types.Message, state: FSMContext):
    await state.update_data(msg_ans = message.text)
    data = await state.get_data()
    if data['msg_ans'] == 'Скачать всю папку' or data['msg_ans'] == 'Скачать файл':
        if PC.is_dir() == True:
            zf = str(str(data['msg_dir']).split('/' or '\\')[-1])
            make_archive(base_name=zf, format='zip', base_dir=PC.current_path, root_dir=PC.current_path,
                         logger=logging.basicConfig(level=logging.INFO))
            time.sleep(1)
            await bot.send_document(message.chat.id, open(pathlib.Path.cwd().joinpath(zf+'.zip'), 'rb'))
            remove(pathlib.Path.cwd().joinpath(f'{zf}.zip'))
            PC.return_home()
            await state.update_data(msg_dir=PC.path)
            await menu(message=message, state=state)
        elif PC.is_dir() == False:
            await bot.send_document(message.chat.id, open(data['msg_dir'], 'rb'))
            PC.return_home()
            await state.update_data(msg_dir=PC.path)
            await menu(message=message, state=state)
        else:
            await message.answer('Упс, что-то пошло не так. Возвращаемся домой.')
            PC.return_home()
            await state.update_data(msg_dir=PC.path)
            await menu(message=message, state=state)
    elif data['msg_ans'] == 'Выбрать файл':
        try:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add('Вернуться домой')
            for file in PC.return_files():
                keyboard.add(types.KeyboardButton(str(file)))
            if PC.return_files() == []:
                await message.answer('У Вас нет здесь файлов :(')
            await message.answer('Пожалуйста выберите файл/папку', reply_markup=keyboard)
            await Form.msg_dir.set()
        except:
            await message.answer('Что-то пошло не так.')
            PC.return_home()
            await state.update_data(msg_dir=PC.path)
            await menu(message=message, state=state)
    elif data['msg_ans'] == 'Вернуться домой':
        PC.return_home()
        await state.update_data(msg_dir=PC.path)
        await menu(message=message, state=state)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Вернуться домой'))
        await message.answer('Пожалуйста пришлите файлы', reply_markup=keyboard)
        async def upload1(message: types.Message, state: FSMContext):
            data = await state.get_data()
            if message.content_type == 'photo':
                file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
                file_name = file_info["file_unique_id"]
                if file_name == data['msg_lf']:
                    await asyncio.sleep(1)
                    await upload1(message=message, state=state)
                else:
                    await state.update_data(msg_lf = file_name)
                    download = await bot.download_file(file_info["file_path"])
                    if PC.current_path != PC.path:
                        with open(f'{PC.choose_fileordir(f"{file_name}")}', 'wb') as new_file:
                            new_file.write(download.getbuffer().tobytes())
                        PC.current_path = PC.current_path.parent
                    else:
                        pass
                    await upload1(message=message, state=state)
            elif message.content_type == 'document':
                file_info = await bot.get_file(message.document.file_id)
                download = await bot.download_file(file_info["file_path"])
                if message.document.file_name == data['msg_lf']:
                    await asyncio.sleep(1)
                    await upload1(message=message, state=state)
                else:
                    await state.update_data(msg_lf =message.document.file_name)
                    if PC.current_path != PC.path:
                        with open(f'{PC.choose_fileordir(f"{message.document.file_name}")}', 'wb') as new_file:
                            new_file.write(download.getbuffer().tobytes())
                        PC.current_path = PC.current_path.parent
                    else:
                        pass
                    await upload1(message=message, state=state)
            elif message.content_type == 'text':
                if message.text == 'Вернуться домой':
                    PC.return_home()
                    await state.update_data(msg_dir=PC.path)
        await upload1(message=message, state=state)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# ReadMe:
# Пожалуйста, для загрузки используйте папку, которая выше корневой на одну.
# Баг заключается в том, что загруженные файлы, могут также загрузиться и в папку ниже(кроме корневой).
# Для правильной закачки, создавайте папку в корневой папке и загружайте в нее,
# Позже манипулируйте с этими файлами, как хотите.