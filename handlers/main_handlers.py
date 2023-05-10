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
    await get_info(query.message,data)
    
    
async def search_patronymic(message: types.Message, state: FSMContext):
    
    await state.update_data(patronymic=message.text)
    data = await state.get_data()
    await state.finish()
    await get_info(message,data)
    

async def get_info(message: types.Message,data):
    response = main_requests.search_employee(data)
    if response:
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
    else:
        await message.answer('Сотрудник не найден!',reply_markup=user_kb.user_keyboard_contact)
# Поиск по подразделению
class fsmSearchUnit(StatesGroup):
    id_unit = State()
    id_department = State()
    surname = State()
    name = State()
    patronymic = State()
async def search_unit(message: types.Message):
    await message.answer('Выберите подразделение, в котором хотите найти сотрудника (напишите цифру):') 
    response = main_requests.search_unit()
    units_count = len(response)
    units = {}
    spisok = ''
    for i in range(units_count):
        units[f'{response[i][0]}'] = response[i][1]
        spisok+=f'''{response[i][0]}. {response[i][1]} \n'''
    await message.answer(spisok)
    await fsmSearchUnit.id_unit.set()


async def search_unit_id(message: types.Message, state: FSMContext):
    await state.update_data(id_unit=message.text)
    data = await state.get_data()
    response = main_requests.search_unit_id(data['id_unit'])
    if response:
        await state.update_data(department=False)
        await message.answer("Выберите отдел (напишите цифру):")
        response = main_requests.search_department()
        units_count = len(response)
        units = {}
        spisok = ''
        for i in range(units_count):
            units[f'{response[i][0]}'] = response[i][2]
            spisok+=f'''{response[i][0]}. {response[i][2]} \n'''
        await message.answer(spisok)
        await fsmSearchUnit.id_department.set()
        
    else:
        await state.update_data(department=False)
        await search_department_id(message,state)

async def search_department_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data['department'] != False:
        await state.update_data(id_department=message.text)
        await message.answer('Введите фамилию сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_surname) 
        await fsmSearchUnit.surname.set()
    else:
        await state.update_data(id_department=None)
        await message.answer('Введите фамилию сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_surname) 
        await fsmSearchUnit.surname.set()
    
async def forgot_surname_unit(query: types.CallbackQuery,state: FSMContext):
    await query.message.edit_text('Введите имя сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_name) 
    await state.update_data(surname=None)
    await fsmSearchUnit.name.set()
    

async def search_surname_unit(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    data = await state.get_data()
    if data['surname']:
        response = main_requests.search_surname(data)
        await message.answer(f'''По запросу {data['surname']} было найдено {response[0]} сотрудников''')
    await message.answer('Введите имя сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_name) 
    await fsmSearchUnit.next()

# Нажатие кнопки забыл имя
async def forgot_name_unit(query: types.CallbackQuery,state: FSMContext):
    await state.update_data(name=None)
    data = await state.get_data()
    if data['surname'] and data['name']==None:
        await query.message.edit_text('Введите отчество сотрудника:') 
        await fsmSearchUnit.patronymic.set()
    else:
        await query.message.edit_text('Введите отчество сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_patronymic) 
        await fsmSearchUnit.patronymic.set()

async def search_name_unit(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    if data['surname'] and data['name']==None:
        await message.answer('Введите отчество сотрудника:') 
        await fsmSearchUnit.patronymic.set()
    elif data['name']:
        response = main_requests.search_name(data)
        await message.answer(f'''По запросу {data['name']} было найдено {response[0]} сотрудников''')
        await message.answer('Введите отчество сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_patronymic) 
        await fsmSearchUnit.patronymic.set()
    else:
        await message.answer('Введите отчество сотрудника:',reply_markup=user_kb.inline_user_keyboard_forgot_patronymic) 
        await fsmSearchUnit.patronymic.set()
# Нажатие кнопки забыл отчество

async def forgot_patronymic_unit(query: types.CallbackQuery,state: FSMContext):
    await state.update_data(patronymic=None)
    data = await state.get_data()
    await state.finish()
    await query.message.delete()
    await get_info_unit(query.message,data)
    
    
async def search_patronymic_unit(message: types.Message, state: FSMContext):
    
    await state.update_data(patronymic=message.text)
    data = await state.get_data()
    await state.finish()
    await get_info_unit(message,data)  

async def get_info_unit(message: types.Message,data):
    response = main_requests.search_employee_unit(data)
    if response:
        await message.answer(data)
        response = main_requests.search_employee(data)
        if response:
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
    else:
        await message.answer('Сотрудник не найден!',reply_markup=user_kb.user_keyboard_contact)

class fsmSearchEmail(StatesGroup):
    email = State()
async def search_email(message: types.Message):
    await message.answer('Введите почту сотрудника:')
    await fsmSearchEmail.email.set()
    
async def search_email_db(message: types.Message,state = FSMContext):
    await state.update_data(mail=message.text)
    data = await state.get_data()
    await state.finish()
    response = main_requests.search_employee(data)
    if response:
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
    else:
        await message.answer('Сотрудник не найден!',reply_markup=user_kb.user_keyboard_contact)
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

    dp.register_message_handler(search_unit,text = "Поиск по подразделению",state=None)
    dp.register_message_handler(search_unit_id,state=fsmSearchUnit.id_unit)
    dp.register_message_handler(search_department_id,state=fsmSearchUnit.id_department)
    dp.register_message_handler(search_surname_unit,state=fsmSearchUnit.surname)
    dp.register_message_handler(search_name_unit,state=fsmSearchUnit.name)
    dp.register_message_handler(search_patronymic_unit,state=fsmSearchUnit.patronymic)
    dp.register_callback_query_handler(forgot_surname_unit,text = "forgot_surname",state=fsmSearchUnit.surname)
    dp.register_callback_query_handler(forgot_name_unit,text = "forgot_name",state=fsmSearchUnit.name)
    dp.register_callback_query_handler(forgot_patronymic_unit,text = "forgot_patronymic",state=fsmSearchUnit.patronymic)


    dp.register_message_handler(search_email,text = "Поиск по почте",state=None)
    dp.register_message_handler(search_email_db,state=fsmSearchEmail.email)


    dp.register_message_handler(back,text = "Вернуться в главное меню")
