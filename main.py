import asyncio
import configparser
import requests
import datetime
from aiogram import Bot, Dispatcher, types
from aiocron import crontab

config = configparser.ConfigParser()
config.read('app.config')
# Retrieve API keys from the configuration file
TELEGRAM_BOT_TOKEN = config.get('API_KEYS', 'TELEGRAM_BOT_TOKEN')

# Replace 'YOUR_BOT_TOKEN' and 'your_channel_id' with your actual values
BOT_TOKEN = TELEGRAM_BOT_TOKEN
# Replace YOUR_CHANNEL_ID
CHANNEL_ID = '1002043368543'
# Replace API
BITCOIN_API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def send_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    data = response.json()
    bitcoin_price = data['bpi']['USD']['rate']
    await bot.send_message(chat_id=CHANNEL_ID, text=f'Текущий курс биткоина: {bitcoin_price} USD')


@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    await message.reply("Привет! Этот бот отправляет курс биткоина в ваш канал каждую минуту.")


async def scheduler():
    # Schedule the task using aiocron
    crontab('*/1 * * * *', send_bitcoin_price, tz=datetime.datetime.now().astimezone().tzinfo)

    while True:
        await asyncio.sleep(60)  # Sleep for 60 seconds


def main():
    # Start the scheduler
    asyncio.get_event_loop().run_until_complete(scheduler())


if __name__ == '__main__':
    main()
