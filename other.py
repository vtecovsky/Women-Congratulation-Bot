from random import randint

from aiogram.dispatcher.filters import Text
import data_base
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None
show_callback_alert = True


class FSMAdmin(StatesGroup):
    text = State()


async def check_admin(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Hello, Admin!')


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.text.set()
        await message.reply('Напишите комплимент ')


async def load_compliments(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['compliment_text'] = message.text
        await message.reply('Комплимент был успешно добавлен в базу ')
        await state.finish()


# @dp.callback_query_handler(Text('compl'))
async def show_info_callback(callback: types.CallbackQuery):
    global show_callback_alert
    db = data_base.sql_read()
    await callback.message.answer(str(db[randint(0, len(db) - 1)]).replace('(', '').replace(')', '')[1:-2])
    await callback.answer(
        text='Надеюсь, тебе понравилось.\nТы можешь получить еще больше приятных слов, нажав на кнопку, но всех их не хватит, чтобы описать тебя!',
        show_alert=show_callback_alert
    )
    show_callback_alert = False


# @dp.message(Command("compliment"))
async def show_info(message: types.Message):
    await bot.send_message(message.chat.id, text='Нажми на кнопку, чтобы получить комплимент!',
                           reply_markup=InlineKeyboardMarkup(). \
                           add(InlineKeyboardButton('Нажми на меня', callback_data='compl')))


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(show_info, commands='compliment')
    dp.register_callback_query_handler(show_info_callback, Text('compl'))
    dp.register_message_handler(check_admin, commands='moderator', is_chat_admin=True)
    dp.register_message_handler(cm_start, commands='Загрузить')
    dp.register_message_handler(load_compliments, state=FSMAdmin)
