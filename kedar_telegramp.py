import requests
import smtplib
import ssl
import urllib3
from bs4 import BeautifulSoup

import time


msg = "please check code"
tele_auth_token = "6365846150:AAHhDMqx6bVwVeOHl_IIOa1t-4l_tEBX9es" # Authentication token provided by Telegram bot
tel_group_id = "-4106448114"     # Telegram group name

def send_msg_on_telegram(msg):
    telegram_api_url = f"https://api.telegram.org/bot{tele_auth_token}/sendMessage?chat_id={tel_group_id}&text={msg}"
    print(telegram_api_url)
    tel_resp = requests.get(telegram_api_url)

    if tel_resp.status_code == 200:
        print ("Notification has been sent on Telegram") 
    else:
        print ("Could not send Message")


class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session



SOON = "Yamunotri and Gangotri  will be announced soon"
URL = "https://registrationandtouristcare.uk.gov.in/index.php"

while True:
    res = get_legacy_session().get(URL)
    # with open('kedd.txt', 'w') as file:
    #     file.write(str(res.content))
    soup = BeautifulSoup(res.content, 'lxml')
    marquee = soup.find_all("span", class_="chardham-marquee-title")
    vals = []


    for i in marquee:
        vals.append(i.get_text())
    isPresent = False
    for val in vals:
        isPresent = SOON in val
        if isPresent:
            break
    print(isPresent)
    if(not isPresent):
        ## send message to telegram bot
        send_msg_on_telegram(f'hurry, booking is opened{URL}')
    
    else:
        ## send failure message to telegram bot
        send_msg_on_telegram('relax and chill')
        
    time.sleep(120)
    print("Program execution resumed after sleeping for 2 minutes.")