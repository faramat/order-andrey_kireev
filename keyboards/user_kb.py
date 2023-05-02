from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
#клавиатура администратора
# user_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
# button_admins = KeyboardButton('Test1')
# user_keyboard.row(button_admins)

#Клавиатура начальная
user_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_contact_info = KeyboardButton('Контактная информация')
button_help = KeyboardButton('Помощь с системой')
user_keyboard.row(button_contact_info).row(button_help)
#Инлайн клавиатура Помощь с системой 
inline_user_keyboard_help = InlineKeyboardMarkup()
button_forgot_password = InlineKeyboardButton('Забыл пароль', callback_data='forgot_password',url='google.com')
button_navigation = InlineKeyboardButton('Навигация в системе', callback_data='navigation',url='vk.com')
button_create_program = InlineKeyboardButton('Создать свою программу', callback_data='create_program',url='youtube.com')
inline_user_keyboard_help.row(button_forgot_password).row(button_navigation).row(button_create_program)
#Клавиатура Контактная информация
user_keyboard_contact = ReplyKeyboardMarkup(resize_keyboard=True)
button_search_fio = KeyboardButton('Поиск по ФИО')
button_search_unit = KeyboardButton('Поиск по подразделению')
button_search_email = KeyboardButton('Поиск по почте')
button_back = KeyboardButton('Вернуться в главное меню')
user_keyboard_contact.row(button_search_fio).row(button_search_unit).row(button_search_email).row(button_back)
#Инлайн клавиатура поиск по фио
inline_user_keyboard_forgot_surname = InlineKeyboardMarkup()
button_forgot_surname = InlineKeyboardButton('Не знаю/Не помню фамилию', callback_data='forgot_surname')
inline_user_keyboard_forgot_surname.row(button_forgot_surname)

inline_user_keyboard_forgot_name = InlineKeyboardMarkup()
button_forgot_name = InlineKeyboardButton('Не знаю/Не помню имя', callback_data='forgot_name')
inline_user_keyboard_forgot_name.row(button_forgot_name)

inline_user_keyboard_forgot_patronymic = InlineKeyboardMarkup()
button_forgot_patronymic = InlineKeyboardButton('Не знаю/Не помню отчество', callback_data='forgot_patronymic')
inline_user_keyboard_forgot_patronymic.row(button_forgot_patronymic)