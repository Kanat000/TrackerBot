from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

bot = Bot(token=config.bot_token, parse_mode="HTML")
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
