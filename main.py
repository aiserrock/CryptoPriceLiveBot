import asyncio
import aiocron
import requests
from aiogram import Bot, Dispatcher
from aiogram.utils import executor

from const import BOT_TOKEN,CHANNEL_ID, AKBARS_BEST_USD_PRICE, MY_ID, HEADERS, CBRF

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def _get_cache_prise() -> float:
    result = requests.get(AKBARS_BEST_USD_PRICE, headers=HEADERS)
    data = result.json()
    cache_usd_price = round(data['branches'][0]['sellPrice'], 2)
    return cache_usd_price


async def _get_cbrf_prise() -> float:
    cbrf = requests.get(CBRF, headers=HEADERS)
    cbrf_data = cbrf.json()
    cbrf_usd_price = round(cbrf_data['Valute']['USD']['Value'], 2)
    return cbrf_usd_price


async def _send_message_to_ls():
    try:
        cbrf = await _get_cbrf_prise()
        cache = await _get_cache_prise()
    except Exception:
        cbrf = cache = 0.0
    diff = round(abs(cbrf - cache), 2)
    message = f'{cache} ₽ - Кеш в обменнике \n{cbrf} ₽ - ЦБ РФ\n{diff} ₽ - Дифф'
    await bot.send_message(chat_id=CHANNEL_ID, text=message)
    print(message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    aiocron.crontab('*/1 * * * *', func=_send_message_to_ls, loop=loop)
    executor.start_polling(dp)
    loop.run_forever()
