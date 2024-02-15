## Bitcoin Ethereum Kaspa Ton live price

[telegram channel](https://t.me/crypto_price_puls)

Get started:
1. cd to CryptoPricePulsBot directory
2. you should rename .env_template to .env and put inside:  
  2.1 your telegram bot token  
  2.2 your telegram channel id  
  2.3 your livepriceapi token  
   
3. `pip install -r requirements.txt`
4. `python3 main.py`

or if your use docker:
1. `docker-compose up -d --build`

### if it don't work use:
1. `docker build --network=host -t cryptopricelivebot:latest .`
2. `docker run -d --restart unless-stopped --network host 92434c2a30d786b9c3e3f0632422bc535bc2b7573c171ced266e1f2dee9cad5e`
