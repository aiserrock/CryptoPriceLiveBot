import os
import asyncio
import aiocron
import requests
import json
from aiogram import Bot, Dispatcher
from aiogram.utils import executor

from const import BOT_TOKEN, LIVEPRICE_API_KEY, LIVEPRICE_API_URL, CHANNEL_ID, AKBARS_BEST_USD_PRICE, \
    MY_ID, HEADERS, proxies, CBRF

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def _get_data() -> list:
    payload = json.dumps({
        "codes": ["BTC", "ETH", "KAS", "TONCOIN", "_GRAM", "CAS"],
        "currency": "USD",
        "sort": "age",
        "order": "descending",
    })
    headers = {
        'content-type': 'application/json',
        'x-api-key': LIVEPRICE_API_KEY
    }

    liveprice_response = requests.request("POST", LIVEPRICE_API_URL, headers=headers, data=payload)
    return liveprice_response.json()


def _make_currencies_price_message(liveprice_data: list) -> str:
    bitcoin_price = round(liveprice_data[0]['rate'])
    ethereum_price = round(liveprice_data[1]['rate'])
    ton_price = round(liveprice_data[3]['rate'], 1)
    kaspa_price = round(liveprice_data[4]['rate'], 2)
    gram_price = round(liveprice_data[5]['rate'], 3)
    kaspa_classic_price = round(liveprice_data[2]['rate'], 4)
    message = f'• BTC: ${bitcoin_price}\n• ETH: ${ethereum_price}\n• TON: ${ton_price}\n• KSP: ${kaspa_price}\n• GRAM: ${gram_price}\n• CAS: ${kaspa_classic_price}'
    return message


async def _send_message_to_channel(message: str):
    await bot.send_message(chat_id=CHANNEL_ID, text=message)
    print(message)
    print('everything is working good! Next message will appear after 59 seconds')

async def _iterate():
    try:
        liveprice_data = await _get_data()
        message = _make_currencies_price_message(liveprice_data)
        await _send_message_to_channel(message)
    except Exception:
        pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    aiocron.crontab('*/1 * * * *', func=_iterate, loop=loop)
    executor.start_polling(dp)
    loop.run_forever()
