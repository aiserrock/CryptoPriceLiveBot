import requests
import pytz
import os
from dotenv import load_dotenv
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

# Read API keys from config file
load_dotenv()

# https://www.coingecko.com/api/documentation
# /simple/price
API_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum%2Cthe-open-network%2Ckaspa%2Cgram-2' \
          '&vs_currencies=usd&include_market_cap=false&include_24hr_vol=false&include_24hr_change=false' \
          '&include_last_updated_at=false&precision=full'
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = '-1002043368543'

bot = Bot(token=BOT_TOKEN)


def send_crypto_prices():
    response = requests.get(API_URL)
    data = response.json()
    bitcoin_price = round(data['bitcoin']['usd'])
    ethereum_price = round(data['ethereum']['usd'])
    ton_price = round(data['the-open-network']['usd'], 2)
    kaspa_price = round(data['kaspa']['usd'], 3)
    gram_price = round(data['gram-2']['usd'], 4)

    message = f'• BTC: ${bitcoin_price}\n• ETH: ${ethereum_price}\n• TON: ${ton_price}\n• KSP: ${kaspa_price}\n• GRAM: ${gram_price}'
    bot.send_message(chat_id=CHANNEL_ID, text=message)


def main():
    scheduler = BlockingScheduler(timezone=pytz.utc)
    scheduler.add_job(send_crypto_prices, 'interval', minutes=1)
    scheduler.start()


if __name__ == '__main__':
    main()
