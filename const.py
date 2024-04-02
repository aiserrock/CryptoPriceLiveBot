from dotenv import load_dotenv
from fake_useragent import UserAgent
import os

# Read API keys from config file
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
LIVEPRICE_API_KEY = os.getenv('LIVEPRICE_API_KEY')
MY_ID = os.getenv('MY_ID')

# https://livecoinwatch.github.io/lcw-api-docs/?python#coinslist
LIVEPRICE_API_URL = "https://api.livecoinwatch.com/coins/map"

HEADERS = {"User-Agent": UserAgent().random}

# https://www.akbars.ru/offices/currency/
AKBARS_BEST_USD_PRICE = 'https://www.akbars.ru/api/v2/offices/bestrates?cityFiasRef=6b1bab7d-ee45-4168-a2a6-4ce2880d90d3&currencycode=USD'
CBRF = 'https://www.cbr-xml-daily.ru/daily_json.js'

# public free rus proxy for akbars: https://www.freeproxy.world/?type=&anonymity=&country=RU&speed=&port=&page=1
proxy_ip = os.getenv('PROXY_IP')
proxy_port = os.getenv('PROXY_PORT')
proxy_login = os.getenv('PROXY_LOGIN')
proxy_password = os.getenv('PROXY_PASSWORD')

proxies = {
    'http': f'socks5://{proxy_login}{proxy_password}@{proxy_ip}:{proxy_port}',
    'https': f'socks5://{proxy_login}{proxy_password}@{proxy_ip}:{proxy_port}',
}
