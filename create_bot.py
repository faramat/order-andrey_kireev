import types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher, storage
from config import botToken
from aiogram.contrib.fsm_storage.memory import MemoryStorage #хранение в оперативке
from aiogram.types import ParseMode

storage=MemoryStorage()
bot = Bot(token=botToken,parse_mode=ParseMode.HTML)
dp = Dispatcher(bot,storage=storage) 