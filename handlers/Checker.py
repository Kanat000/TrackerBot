from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from loader import dp, bot
from handlers.keyboards import replyKeyboard
import re
from Database.dbConnection import SQLite
from config import dbName, admin_id
from handlers.Parser import TelegramParser

db = SQLite(dbName)


class Form(StatesGroup):
    nick_name = State()
    delete_nick = State()


@dp.message_handler(Command("start"))
async def start_bot(message: Message, state: FSMContext):
    await state.reset_state(True)
    db.create_Nicknames_table()
    await message.answer("\U0001F44B<b> Привет. Я ник-чекер бот."
                         "При освобождении никнейма из вашего списка я буду вас уведомлять.</b>\n"
                         "Чтобы начать слежку, добавьте новые занятые никнеймы.",
                         reply_markup=replyKeyboard.reply_keyboard)


@dp.message_handler(text="Добавить новый Ник-нэйм")
@dp.message_handler(Command('add_new_nickname'))
async def add_new_nick(message: Message):
    await Form.nick_name.set()
    await message.answer("<b>Пожалуйста, отправьте никнейм (без символа @), который вы хотите отслеживать:</b>\n"
                         "Никнейм должен содержать минимум 5 и максимум 32 символа (A-Z, a-z, 0-9 и _).",
                         reply_markup=replyKeyboard.cancel_reply_keyboard)


@dp.message_handler(state=Form.nick_name)
async def save_nick_name(message: Message, state: FSMContext):
    try:
        if message.text != 'Отмена':
            async with state.proxy() as data:
                nick_name = message.text
                nick_pattern = re.compile("[a-z0-9_]+")
                if len(nick_name) > 5 and nick_pattern.fullmatch(nick_name):
                    telegram_parser = TelegramParser()
                    if telegram_parser.parse_nickname(nick_name) > 0:
                        chat_id = message.chat.id
                        if not db.exists_nickname_for_chat(nick_name, chat_id):
                            data['nick_name'] = nick_name
                            await state.finish()
                            db.insert_nickname(data['nick_name'], chat_id)
                            await message.answer("<b>Отлично, никнейм сохранен! </b>\n"
                                                 "Вам придет уведомление, когда введенный вами никнейм освободиться.",
                                                 reply_markup=replyKeyboard.reply_keyboard)
                        else:
                            await state.finish()
                            await message.answer("Данный никнейм уже занесен в ваш список.",
                                                 reply_markup=replyKeyboard.reply_keyboard)
                    else:
                        await state.finish()
                        await message.answer("Данный никнейм свободен.", reply_markup=replyKeyboard.reply_keyboard)
                else:
                    await Form.nick_name.set()
                    await message.answer(
                        "Вы ввели неправильный никнейм! "
                        "Никнейм должен содержать минимум 5 и максимум 32 символа  (A-Z, a-z, 0-9 и _)."
                        "\n Пожалуйста, попробуйте снова (без символа '@'):",
                        reply_markup=replyKeyboard.cancel_reply_keyboard)
        else:
            await state.finish()
            await message.answer(text='Действие отменено. Что дальше?', reply_markup=replyKeyboard.reply_keyboard)
    except Exception as e:
        await bot.send_message(admin_id, str(e))


@dp.message_handler(text="Мой список Ник-нэймов")
@dp.message_handler(Command('my_list_of_nicknames'))
async def my_list_of_nicknames(message: Message):
    try:
        nickname_list = db.get_nickname_list_for_chat_id(message.chat.id)
        if len(nickname_list) > 0:
            msg_template = "<b>Ваш cписок никнеймов для отслеживания:</b>\n"
            for nickname in nickname_list:
                index = nickname_list.index(nickname) + 1
                msg_template += str(index) + '. ' + nickname[0] + '\n'

            await message.answer(msg_template, reply_markup=replyKeyboard.reply_keyboard)
        else:
            await message.answer("Ваш список пуст. Для отображения списка, добавьте хотя бы один никнейм.",
                                 reply_markup=replyKeyboard.reply_keyboard)
    except Exception as e:
        await bot.send_message(admin_id, str(e))


@dp.message_handler(text="Удалить Ник-нэйм")
@dp.message_handler(Command('delete_nickname'))
async def delete_nickname(message: Message):
    try:
        nickname_list = db.get_nickname_list_for_chat_id(message.chat.id)
        if len(nickname_list) > 0:
            msg_template = "\n<b>Ваш список: </b> \n"
            for nickname in nickname_list:
                index = nickname_list.index(nickname) + 1
                msg_template += str(index) + '. ' + nickname[0] + '\n'

            await Form.delete_nick.set()
            await message.answer("<b>Какой никнейм вы хотите удалить из списка?</b>\n" + msg_template,
                                 reply_markup=replyKeyboard.cancel_reply_keyboard)
        else:
            await message.answer("Ваш список пуст. Для отображения списка, добавьте хотя бы один никнейм.",
                                 reply_markup=replyKeyboard.reply_keyboard)
    except Exception as e:
        await bot.send_message(admin_id, str(e))


@dp.message_handler(state=Form.delete_nick)
async def delete_nickname_from_db(message: Message, state: FSMContext):
    try:
        if message.text != 'Отмена':
            async with state.proxy() as data:
                db_nickname_list = db.get_nickname_list_for_chat_id(message.chat.id)
                nickname = message.text
                nickname_list = []
                for nick in db_nickname_list:
                    nickname_list.append(nick[0])

                if nickname in nickname_list:
                    db.delete_nickname(nickname, message.chat.id)
                    await state.finish()
                    await message.answer(f"'{nickname}' удачно удалено из вашего списка! Вам что то еще нужно?",
                                         reply_markup=replyKeyboard.reply_keyboard)
                else:
                    await Form.delete_nick.set()
                    await message.answer(f"Данный никнейм нет в вашем списке. Повтарите попытку:",
                                         reply_markup=replyKeyboard.reply_keyboard)
        else:
            await state.finish()
            await message.answer("Действие отменено. Что дальше?", reply_markup=replyKeyboard.reply_keyboard)
    except Exception as e:
        await bot.send_message(admin_id, str(e))
