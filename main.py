from aiogram.utils import executor
from create_bot import dp
from data_base import main_requests
from handlers import main_handlers

async def on_startup(_):
    response = main_requests.sql_start()
    if response:
        print('Bot online. OK!')
    else:
        print('Not ok!')

main_handlers.register_handlers_main(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True,on_startup=on_startup)




