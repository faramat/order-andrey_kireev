#----
#ТГ
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove,CallbackQuery
#БД
from data_base import main_requests
#Клавиатуры
from keyboards import *
#Машина состояний 
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup 
#Другое

#----
async def start(message: types.Message):
    await message.answer('Hello!', reply_markup=user_kb.user_keyboard)

# Бэк Помощь с системой
async def help(message: types.Message):
    await message.answer('Какая помощь Вам нужна?',reply_markup=user_kb.inline_user_keyboard_help)

async def forgot_password(query: types.CallbackQuery):
    await bot.edit_message_reply_markup(query.from_user.id,query.message.message_id,reply_markup=user_kb.user_keyboard)

async def navigation(query: types.CallbackQuery):
    await bot.edit_message_reply_markup(query.from_user.id,query.message.message_id,reply_markup=user_kb.user_keyboard)

async def create_program(query: types.CallbackQuery):
    await bot.edit_message_reply_markup(query.from_user.id,query.message.message_id,reply_markup=user_kb.user_keyboard)

# Бэк Контактная информация
async def contact_info(message: types.Message):
    await message.answer('done',reply_markup=user_kb.user_keyboard_contact)
# Поиск по фио
class fsmSearchFio(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()

async def search_fio(message: types.Message):
    await message.answer('Введите фамилию сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_surname) 
    await fsmSearchFio.surname.set()
    
# Нажатие кнопки забыл фамилию
async def forgot_surname(query: types.CallbackQuery,state: FSMContext):
    await query.message.edit_text('Введите имя сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_name) 
    await state.update_data(surname=None)
    await fsmSearchFio.name.set()
    

async def search_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    data = await state.get_data()
    if data['surname']:
        response = main_requests.search_surname(data)
        await message.answer(f'''По запросу {data['surname']} было найдено {response[0]} сотрудников''')
    await message.answer('Введите имя сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_name) 
    await fsmSearchFio.next()

# Нажатие кнопки забыл имя
async def forgot_name(query: types.CallbackQuery,state: FSMContext):
    await state.update_data(name=None)
    data = await state.get_data()
    if data['surname'] and data['name']==None:
        await query.message.edit_text('Введите отчество сотрудника:') 
        await fsmSearchFio.patronymic.set()
    else:
        await query.message.edit_text('Введите отчество сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_patronymic) 
        await fsmSearchFio.patronymic.set()

async def search_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    if data['surname'] and data['name']==None:
        await message.answer('Введите отчество сотрудника:') 
        await fsmSearchFio.patronymic.set()
    elif data['name']:
        response = main_requests.search_name(data)
        await message.answer(f'''По запросу {data['name']} было найдено {response[0]} сотрудников''')
        await message.answer('Введите отчество сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_patronymic) 
        await fsmSearchFio.patronymic.set()
    else:
        await message.answer('Введите отчество сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_patronymic) 
        await fsmSearchFio.patronymic.set()
# Нажатие кнопки забыл отчество

async def forgot_patronymic(query: types.CallbackQuery,state: FSMContext):
    await state.update_data(patronymic=None)
    data = await state.get_data()
    await state.finish()
    await query.message.delete()
    response = main_requests.search_employee(data)
    await query.message.answer(response,reply_markup=user_kb.user_keyboard_contact)
    
async def search_patronymic(message: types.Message, state: FSMContext):
    await state.update_data(patronymic=message.text)
    data = await state.get_data()
    await state.finish()
    response = main_requests.search_employee(data)
    await message.answer(f'''
ФИО: {response[0]} {response[1]} {response[2]} \n
Подразделение: {response[9]} \n
Отдел: {response[10]} \n
Должность: {response[11]} \n
Почта: {response[3]} \n
Телефон: {response[5]} \n
Внутренний номер: {response[6]} \n
Здание: {response[7]} \n
Кабинет: {response[4]} \n 
Адрес: {response[8]} \n
    ''',reply_markup=user_kb.user_keyboard_contact)

    







async def search_unit(message: types.Message):
    await message.answer('done') 

async def search_email(message: types.Message):
    await message.answer('done') 

async def back(message: types.Message):
    await start(message)
#регистрация функций для дальнейшей передачи
def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start,commands = ['start'])
    dp.register_message_handler(help,text = "Помощь с системой")
    dp.register_callback_query_handler(forgot_password,text = "forgot_password")
    dp.register_callback_query_handler(navigation,text = "navigation")
    dp.register_callback_query_handler(create_program,text = "create_program")

    dp.register_message_handler(contact_info,text = "Контактная информация")
    dp.register_message_handler(search_fio,text = "Поиск по ФИО",state=None)
    dp.register_message_handler(search_surname,state=fsmSearchFio.surname)
    dp.register_message_handler(search_name,state=fsmSearchFio.name)
    dp.register_message_handler(search_patronymic,state=fsmSearchFio.patronymic)
    dp.register_callback_query_handler(forgot_surname,text = "forgot_surname",state=fsmSearchFio.surname)
    dp.register_callback_query_handler(forgot_name,text = "forgot_name",state=fsmSearchFio.name)
    dp.register_callback_query_handler(forgot_patronymic,text = "forgot_patronymic",state=fsmSearchFio.patronymic)
    dp.register_message_handler(search_unit,text = "Поиск по подразделению")
    dp.register_message_handler(search_email,text = "Поиск по почте")
    dp.register_message_handler(back,text = "Вернуться в главное меню")
