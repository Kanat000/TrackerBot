from Database.dbConnection import SQLite
from config import dbName
from loader import bot
from handlers.Parser import TelegramParser

db = SQLite(dbName)


async def note():
    telegram_parser = TelegramParser()
    nickname_list = db.select_all_nickname()
    for nick in nickname_list:
        if telegram_parser.parse_nickname(nick[0]) == 0:
            chat_id_list = db.get_chat_id_list_by_nickname(nick[0])
            for chat_id in chat_id_list:
                await bot.send_message(chat_id=chat_id[0], text=f"Освободился никнейм:'{nick[0]}'")
                await bot.send_message(chat_id=chat_id[0], text=f"Никнейм '{nick[0]}' удален из вашего списка.")
                db.delete_nickname(nick[0], chat_id[0])
