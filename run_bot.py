from aiogram.utils import executor
from create_bot import dp
import data_base
import other


async def on_startup(_):
    print('Bot is starting...')
    data_base.sql_start()


other.register_handlers(dp)
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
