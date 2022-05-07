from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

reply_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
reply_keyboard.insert(
    KeyboardButton(text="Добавить новый Ник-нэйм")
)
reply_keyboard.insert(
    KeyboardButton(text="Мой список Ник-нэймов")
)
reply_keyboard.insert(
    KeyboardButton(text="Удалить Ник-нэйм")
)

cancel_reply_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
cancel_reply_keyboard.insert(
    KeyboardButton(text="Отмена")
)
