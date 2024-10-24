#! /usr/bin/env python
#!coding:utf-8
import asyncio
import logging
import sys
import time
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession

from api_pogoda import WeatherFormatter, WeatherAPI
from config import TOKEN, API
from geolocation import logger

# Логирование
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
file_handler = logging.FileHandler('log.log', encoding='utf-8', mode='a')
logger.addHandler(handler)
logger.addHandler(file_handler)

dp = Dispatcher()


# Хэндлер для команды /start
@dp.message(CommandStart())
async def start_command(message: Message):
    try:
        await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды")
    except Exception as e:
        logger.error(f"start command: {e}")


# Хэндлер для получения погоды
@dp.message()
async def get_weather(message: Message):
    try:
        await message.answer(f"Смотрю погоду в городе {message.text}")
        weather_api = WeatherAPI(API, message.text)
        weather_data = weather_api.get_weather_data()
        messag = WeatherFormatter.format_weather_message(weather_data, message.from_user.first_name)
        await message.answer(messag)
    except Exception as e:
        logger.error(f"get_water: {e}")
        await message.answer("Что-то пошло не так! Проверяю!!!")


async def main():
    logger.info(f"Start: {datetime.now()}")
    # Инициализация бота
    """Сессия для сервера pythonanywhere"""
    session = AiohttpSession(
        proxy='http://proxy.server:3128')  # в proxy указан прокси сервер pythonanywhere, он нужен для подключения

    bot = Bot(token=TOKEN, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        # Удаление вебхуков и запуск поллинга
        # await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, polling_timeout=60)
        # await bot.close(request_timeout=10)
    except KeyboardInterrupt:
        logger.error(f"Завершение программы {datetime.now()}")
        await dp.stop_polling()
    except Exception as e:
        logger.error(f"Error: {e}")



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Завершение программы")
        dp.stop_polling()
