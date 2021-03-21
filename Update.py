#!/usr/bin/env python
import json
import random
from DateBase import *

path = os.path.abspath(os.curdir)

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
            dogecoin=random.choice(wallets))
        os.replace(f'{path}/Update/{file}', f'{path}/Data/{file}')