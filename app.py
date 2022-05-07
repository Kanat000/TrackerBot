import asyncio
import time
from threading import Thread

from aiogram import executor
from handlers.Checker import dp
from handlers.Notification import note
import schedule


async def note_every_two_minute():
    while True:
        await note()
        schedule.run_pending()
        await asyncio.sleep(120)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(note_every_two_minute())
    loop.create_task(executor.start_polling(dp))
    loop.run_forever()
