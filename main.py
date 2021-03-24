#!/usr/bin/env python
from pyrogram import Client, filters
from multiprocessing import Process
from pyrogram.errors import FloodWait
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import time
import undetected_chromedriver as uc
from DateBase import *
import json
import random
from colorama import Fore, init
import sys
import re
import os
import shutil
init(autoreset=True)

def bot_job(phone):

    app = Client(
        session_name=phone,
        api_id=get_api_id(phone),
        api_hash=get_api_hash(phone),
        app_version=get_app_version(phone),
        device_model=get_device_model(phone),
        system_version=get_system_version(phone),
        lang_code='en',
        workdir=f'{path}/Session/')

    global counter, chanel_id

    scheduler = AsyncIOScheduler()
    scheduler.start()

    @scheduler.scheduled_job('interval', seconds=1500, start_date=f'{datetime.now() + timedelta(seconds=3)}')
    def bot_start():

        global counter
        counter = 0

        user = app.get_me()['first_name']
        print(Fore.BLUE + f"{user} entered Telegram")

        Ids = get_id_key(phone)
        for id in Ids:
            timer = get_timer(id)
            if timer < round(time.time()):
                chanel = get_chanel_id(id)
                try:
                    app.leave_chat(chanel)
                    chanel_delete(id, phone, chanel)
                except Exception as error:
                    print(Fore.RED + f'{error}')
                    if 'USER_NOT_PARTICIPANT' in str(error):
                        chanel_delete(id, phone, chanel)
                    elif 'CHANNEL_INVALID' in str(error):
                        chanel_delete(id, phone, chanel)
                    elif 'CHANNEL_PRIVATE' in str(error):
                        chanel_delete(id, phone, chanel)
        try:
            app.send_message('Dogecoin_click_bot', '🖥 Visit sites')
        except Exception as error:
            print(Fore.RED + f'{error}')
            sys.exit()

    @app.on_message(filters.chat(715510199) & filters.regex('Press the "Visit website" button'))
    def log(app, message):
        global counter
        if counter == 0:
            counter = 1
            url = re.findall(r'http[s]?://doge.click/v\w+/\w+', f'{str(message)}')[0]
            if 'visit' in url:
                chrome.get(url)
                try:
                    timer = chrome.find_element_by_id('headbar')
                    t_wait = int(timer.get_attribute("data-timer"))
                    print(Fore.RED + f'TIMER {t_wait}')
                    time.sleep(t_wait + 5)
                except:
                    pass
            else:
                print(Fore.YELLOW + 'DDoS on VISIT')
                message.click('⏩ Skip')
        else:
            app.send_message(715510199, '🤖 Message bots')

    @app.on_message(filters.chat(715510199) & filters.regex('Press the "Message bot" botton'))
    def log(app, message):
        global counter
        if counter == 1:
            counter = 2
            url = re.findall(r'http[s]?://doge.click/b\w+/\w+', f'{str(message)}')[0]
            if 'doge.click/bot' in url:
                chrome.get(url)
                site = chrome.page_source
                bot = re.findall(r'Telegram: Contact @(.*)<', site)[0]
                try:
                    bot_init_message = app.send_message(f'{bot}', '/start')
                    bot_id = bot_init_message["chat"]["id"]
                    bot_init_message_id = bot_init_message["message_id"]
                    time.sleep(10)
                    for message_to_forward in app.iter_history(bot_id, limit=1):
                        message_to_forward_id = message_to_forward["message_id"]
                        if bot_init_message_id != message_to_forward_id:
                            app.forward_messages(715510199, 'me', message_to_forward_id)
                        else:
                            message.click('⏩ Skip')
                    app.block_user(bot_id)
                except FloodWait as error:
                    counter = 3
                    print(Fore.RED + f'{error}')
                    app.send_message(715510199, '💰 Balance')
                except Exception as error:
                    print(Fore.RED + f'{error}')
                    message.click('⏩ Skip')
            else:
                print(Fore.YELLOW + 'DDoS on Bot')
                message.click('⏩ Skip')
        else:
            app.send_message(715510199, '📣 Join chats')

    @app.on_message(filters.chat(715510199) & filters.regex('After joining, press the "Joined"'))
    def log(app, message):
        global counter, chanel_id
        if counter == 2:
            url = re.findall(r'http[s]?://doge.click/j\w+/\w+', f'{str(message)}')[0]
            if 'join' in url:
                chrome.get(url)
                site = chrome.page_source
                try:
                    chanel = re.findall(r'Telegram: Contact @(.*)<', site)[0]
                    chat = app.join_chat(f'{chanel}')
                    chanel_id = chat['id']
                    timer = round(time.time())
                    chanel_insert(phone, chanel_id, timer)
                    message.click('✅ Joined')
                except FloodWait as error:
                    print(Fore.RED + f'{error}')
                    counter = 3
                    app.send_message(715510199, '💰 Balance')
                except Exception as error:
                    print(Fore.RED + f'{error}')
                    message.click('⏩ Skip')
            else:
                print(Fore.YELLOW + 'DDoS on JOIN')
                message.click('⏩ Skip')


    @app.on_message(filters.chat(715510199) & filters.regex('Use /join to get a new one'))
    def log(app, message):
        app.send_message(715510199, '/join')

    @app.on_message(filters.chat(715510199) & filters.regex('Available balance:'))
    def log(app, message):
        if counter == 3:
            balance = float(re.findall(r'Available balance: (.*) DOGE', message["text"])[0])
            print(Fore.GREEN + f'{message["text"]}')
            if balance > 2.1:
                message.click('💵 Withdraw')
            else:
                sys.exit()

    @app.on_message(filters.chat(715510199) & filters.regex('enter your Dogecoin address:'))
    def log(app, message):
        wallet = get_wallet(phone)
        app.send_message(715510199, f'{wallet}')

    @app.on_message(filters.chat(715510199) & filters.regex('Enter the amount to withdraw'))
    def log(app, message):
        message.click('💰 Max amount')

    @app.on_message(filters.chat(715510199) & filters.regex('you sure you want to send'))
    def log(app, message):
        message.click('✅ Confirm')
        sys.exit()

    @app.on_message(filters.chat(715510199) & filters.regex('You must stay in the'))
    def log(app, message):
        global chanel_id
        timer = (int(re.findall(r'(\d+) hour', f'{message["text"]}')[0])*3600)+round(time.time())
        chanel_upgrade(phone, chanel_id, timer)

    @app.on_message(filters.chat(715510199) & filters.regex('click tasks are'))
    def log(app, message):
        global counter
        if counter == 1:
            pass
        else:
            counter = 1
            print(Fore.RED + f'{phone} no CLICK avalible')
            app.send_message(715510199, '🤖 Message bots')

    @app.on_message(filters.chat(715510199) & filters.regex('bot tasks are'))
    def log(app, message):
        global counter
        if counter == 2:
            pass
        else:
            counter = 2
            print(Fore.RED + f'{phone} no BOT avalible')
            app.send_message(715510199, '📣 Join chats')

    @app.on_message(filters.chat(715510199) & filters.regex('join tasks are'))
    def log(app, message):
        global counter
        counter = 3
        print(Fore.RED + f'{phone} no JOIN avalible')
        app.send_message(715510199, '💰 Balance')

    @app.on_message(filters.chat(715510199) & filters.regex('for visiting a site!'))
    def log(app, message):
        print(Fore.GREEN + f'{message["text"]}')

    @app.on_message(filters.chat(715510199) & filters.regex('for messaging a bot!'))
    def log(app, message):
        print(Fore.GREEN + f'{message["text"]}')

    try:
        app.run()
    except Exception as error:
        print(Fore.RED + f'{phone}: {error}')
        if '401 USER_DEACTIVATED_BAN' in str(error):
            account_delete(phone)
            os.replace(f'{path}/Session/{phone}.session', f'{path}/Banned/{phone}.session')
            os.replace(f'{path}/Data/{phone}.json', f'{path}/Banned/{phone}.json')


make_tables()

with open(f'{path}/Data/Doge_Wallet.txt', 'r') as inf:
    wallets = inf.readlines()

for root, dirs, files in os.walk(f'{path}/Update/'):
    for file in files:
        with open(f'{path}/Update/{file}', 'r') as inf:
            db_add = json.load(inf)
        account_insert(
            phone=db_add['phone'],
            api_id=db_add['api_id'],
            api_hash=db_add['api_hash'],
            app_version=db_add['app_version'],
            device_model=db_add['device_model'],
            system_version=db_add['system_version'],
            wallet=random.choice(wallets))
        os.replace(f'{path}/Update/{file}', f'{path}/Data/{file}')

try:
    shutil.rmtree(f'{path}/Browser')
except:
    pass
finally:
    os.makedirs(f'{path}/Browser')

try:
    options = uc.ChromeOptions()
    #options.add_argument("--start-maximized")
    #options.add_argument("--no-sandbox")
    #options.add_argument("--disable-extensions")
    options.headless = True
    options.add_argument("--headless")
    options.add_argument(f"--user-data-dir={path}/Browser")
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    chrome = uc.Chrome(options=options)
    chrome.implicitly_wait(10)
except Exception as error:
    print(Fore.RED + f'{error}')
    sys.exit()

Phones = table_read_row(row='PHONE', table='accounts')
print(Fore.BLUE + f'All account count = {len(Phones)}')
for phone in Phones:
    if __name__ == '__main__':
        bot = Process(target=bot_job, args=(phone,))
        bot.start()
        bot.join()