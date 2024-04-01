import os
import asyncio
import aiocron
import requests
import json
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

# Read API keys from config file
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
LIVEPRICE_API_KEY = os.getenv('LIVEPRICE_API_KEY')
MY_ID = os.getenv('MY_ID')

# https://livecoinwatch.github.io/lcw-api-docs/?python#coinslist
LIVEPRICE_API_URL = "https://api.livecoinwatch.com/coins/map"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
session = HTTP()


async def send_price():
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
    liveprice_data = liveprice_response.json()

    bitcoin_price = round(liveprice_data[0]['rate'])
    ethereum_price = round(liveprice_data[1]['rate'])
    ton_price = round(liveprice_data[2]['rate'], 1)
    kaspa_price = round(liveprice_data[3]['rate'], 2)
    gram_price = round(liveprice_data[4]['rate'], 3)
    kaspa_classic_price = round(liveprice_data[5]['rate'], 4)
    message = f'• BTC: ${bitcoin_price}\n• ETH: ${ethereum_price}\n• TON: ${ton_price}\n• KSP: ${kaspa_price}\n• GRAM: ${gram_price}\n• CAS: ${kaspa_classic_price}'
    await bot.send_message(chat_id=CHANNEL_ID, text=message)
    print(message)
    print('everything is working good! Next message will appear after 59 seconds')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Schedule the task to run every minute
    aiocron.crontab('*/1 * * * *', func=send_price, loop=loop)
    executor.start_polling(dp)
    loop.run_forever()
