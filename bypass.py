import asyncio
import os
import re
import time
import aiohttp
import requests
import aiofiles
from base64 import standard_b64encode, standard_b64decode
from pyrogram import Client, filters, idle, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


from config import Config

logging.getLogger("pyrogram").setLevel(logging.WARNING)
app = Client(
            "Bot",
            bot_token = Config.BOT_TOKEN,
            api_id = Config.API_ID,
            api_hash = Config.API_HASH)

import re
from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# ouo url
# Examples:
# https://ouo.io/HxFVfD - ouo.io links (no account -> only one step)
# https://ouo.press/Zu7Vs5 - ouo.io links (with account -> two steps)
# Can exchange between ouo.press and ouo.io

url = "https://ouo.press/Zu7Vs5"

# -------------------------------------------

def RecaptchaV3():
    import requests
    ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8ucHJlc3M6NDQz&hl=en&v=pCoGBhjs9s8EhFOHJFe8cqis&size=invisible&cb=ahgyd1gkfkhe'
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({
        'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re.findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re.findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer

# -------------------------------------------

client = requests.Session()
client.headers.update({
    'authority': 'ouo.io',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'referer': 'http://www.google.com/ig/adde?moduleurl=',
    'upgrade-insecure-requests': '1',
})

# -------------------------------------------
# OUO BYPASS


def ouo_bypass(url):
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    res = client.get(tempurl, impersonate="chrome110")
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):

        if res.headers.get('Location'): break

        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = { input.get('name'): input.get('value') for input in inputs }
        data['x-token'] = RecaptchaV3()
        
        h = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        
        res = client.post(next_url, data=data, headers=h, 
            allow_redirects=False, impersonate="chrome110")
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"

    return {
        'original_link': url,
        'bypassed_link': res.headers.get('Location')
    }

# -------------------------------------------

out = ouo_bypass(url)
print(out)

# -------------------------------------------
'''
SAMPLE OUTPUT

{
    'original_link': 'https://ouo.io/go/HxFVfD',
    'bypassed_link': 'https://some-link.com'
}

'''
'''
 _._     _,-'""`-._
(,-.`._,'(       |\`-/|
    `-.-' \ )-`( , o o)
          `-    \`_`"'-
'''
def b64_to_str(b64: str) -> str:
    bytes_b64 = b64.encode('ascii')
    bytes_str = standard_b64decode(bytes_b64)
    __str = bytes_str.decode('ascii')
    return __str
def str_to_b64(__str: str) -> str:

    str_bytes = __str.encode('ascii')

    bytes_b64 = standard_b64encode(str_bytes)

    b64 = bytes_b64.decode('ascii')

    return b64

@app.on_message(filters.command("start") & filters.private)
async def start(bot, cmd: Message):
    usr_cmd = cmd.text.split("_", 1)[-1]
    kay_id = -1001642923224
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    if usr_cmd == "/start":
        await cmd.reply_text("""**Meow! Send me "ouo.io" or "ouo.press" & I'll bypass & send you the destination link. 😺**""")
    else:
        try:
            user = await app.get_chat_member(-1001315223923, cmd.from_user.id)
            if user.status == enums.ChatMemberStatus.MEMBER:
                x1 = await cmd.reply_text("`Meow! Bypassing...` 😺\n\n")
                url = (usr_cmd).split("_")[-1]
                bl = ouo_bypass(url)
                asyncio.sleep(3)
                await x1.delete()
                x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot.")
            elif user.status == enums.ChatMemberStatus.ADMINISTRATOR:
                x1 = await cmd.reply_text("`Meow! Bypassing...` 😺")
                url = (usr_cmd).split("_")[-1]
                bl = ouo_bypass(url)
                asyncio.sleep(3)
                await x1.delete()
                x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot.")
            elif user.status == enums.ChatMemberStatus.OWNER:
                x1 = await cmd.reply_text("`Meow! Bypassing...` 😺")
                url = (usr_cmd).split("_")[-1]
                bl = ouo_bypass(url)
                asyncio.sleep(3)
                await x1.delete()
                x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`")
            elif user.status not in (enums.ChatMemberStatus.MEMBER, enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                idk = (usr_cmd).split("_")[-1]  
                idk = idk.replace("https://ouo.io/", "")
                idk = idk.replace("http://ouo.io/", "")
                idk = idk.replace("https://ouo.press/", "")
                idk = idk.replace("http://ouo.press/", "")
                dl_markup = InlineKeyboardMarkup(
                    [
                      [
                        InlineKeyboardButton(text="😼 Channel", url=f"https://t.me/neko_bots"),
                        InlineKeyboardButton(text="🔄 Retry", url=f"https://t.me/ouo_bypass_robot?start=neko_{idk}")
                      ]
                    ]
                )
                meow = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡀⠀⠀⣰⣷⠀⠀⣮⣢⣖⣲⡦⠀⢀⣞⡻⠟⣦⠀⠀⣄⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠟⠅⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡇⠻⡀⡔⠁⢿⠀⠀⡟⠀⠀⠀⠀⢐⡽⠉⠀⠀⢘⣇⠰⡏⠀⠀⢀⠀⠀⠀⣷⠀⠀⢘⡛⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⢿⡇⠀⢿⠀⠀⣿⠿⠻⠿⠀⢘⣫⠀⠀⢀⡼⠕⢘⣇⠀⣐⡿⡄⠀⠀⣭⠀⠀⢘⣗⠂⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⢸⠀⠀⣷⣀⣀⡀⠀⣴⢿⣕⣒⣫⠋⠀⠀⣗⠄⢘⣿⡓⡄⣸⡯⠀⠀⠀⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⠀⠀⠀⠀⢈⡂⠈⠙⠋⠛⠋⡮⠋⠉⢟⣎⠀⠀⠀⠀⠈⠛⠛⠀⠉⠛⠋⠁⠀⢀⣔⡱⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀⠈⢽⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠷⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣞⡏⠉⠙⠷⢆⡀⠀⠀⢀⣀⣦⡧⠭⠝⠿⠵⣷⡏⠀⠀⠀⠀⠀⠿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡜⣷⠀⠀⠀⠀⠙⣧⡞⡉⠃⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢷⣟⠀⠀⠀⠀⠀⠉⠚⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡄⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀⠀⠀⠀⣀⣠⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⣟⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠑⣷⣀⣠⡤⠒⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⣸⡷⠛⠛⠛⠏⠀⠀⠀⠈⠛⢦⣿⣟⡅⠀⠀⡀⣤⡶⠆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡠⣿⡀⠀⣠⡶⠶⠴⣤⣄⠀⠠⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠚⢷⡀⠀⠀⠀⠤⢿⣷⠚⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣷⠃⠀⠘⠛⠀⠀⣀⡼⠿⠃⠀⠀⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢐⡏⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠨⣇⡀⠀⠦⣀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢔⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣔⠞⣽⣟⠊⠱⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⣤⡶⠗⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⠾⠉⠀⣀⣙⣷⠤⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣬⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠘⠉⠀⠀⣀⠞⠁⠙⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣠⡶⠞⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡶⠊⠀⠀⠀⠘⠓⠶⠴⠴⠦⠦⠦⠶⣄⡬⠭⠓⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠁"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                await cmd.reply_text(f"Join [Neko Bots 😼](https://t.me/neko_bots) to access me.\n\n{meow}", reply_markup=dl_markup)
        except Exception as err:
            idk = (usr_cmd).split("_")[-1]  
            dl_markup = InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="😼 Channel", url=f"https://t.me/neko_bots"),
                    InlineKeyboardButton(text="🔄 Retry", url=f"https://t.me/ouo_bypass_robot?start=neko_{idk}")
                  ]
                ]
            )  
            meow = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡀⠀⠀⣰⣷⠀⠀⣮⣢⣖⣲⡦⠀⢀⣞⡻⠟⣦⠀⠀⣄⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠟⠅⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡇⠻⡀⡔⠁⢿⠀⠀⡟⠀⠀⠀⠀⢐⡽⠉⠀⠀⢘⣇⠰⡏⠀⠀⢀⠀⠀⠀⣷⠀⠀⢘⡛⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⢿⡇⠀⢿⠀⠀⣿⠿⠻⠿⠀⢘⣫⠀⠀⢀⡼⠕⢘⣇⠀⣐⡿⡄⠀⠀⣭⠀⠀⢘⣗⠂⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⢸⠀⠀⣷⣀⣀⡀⠀⣴⢿⣕⣒⣫⠋⠀⠀⣗⠄⢘⣿⡓⡄⣸⡯⠀⠀⠀⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⠀⠀⠀⠀⢈⡂⠈⠙⠋⠛⠋⡮⠋⠉⢟⣎⠀⠀⠀⠀⠈⠛⠛⠀⠉⠛⠋⠁⠀⢀⣔⡱⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀⠈⢽⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠷⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣞⡏⠉⠙⠷⢆⡀⠀⠀⢀⣀⣦⡧⠭⠝⠿⠵⣷⡏⠀⠀⠀⠀⠀⠿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡜⣷⠀⠀⠀⠀⠙⣧⡞⡉⠃⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢷⣟⠀⠀⠀⠀⠀⠉⠚⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡄⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀⠀⠀⠀⣀⣠⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⣟⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠑⣷⣀⣠⡤⠒⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⣸⡷⠛⠛⠛⠏⠀⠀⠀⠈⠛⢦⣿⣟⡅⠀⠀⡀⣤⡶⠆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡠⣿⡀⠀⣠⡶⠶⠴⣤⣄⠀⠠⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠚⢷⡀⠀⠀⠀⠤⢿⣷⠚⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣷⠃⠀⠘⠛⠀⠀⣀⡼⠿⠃⠀⠀⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢐⡏⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠨⣇⡀⠀⠦⣀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢔⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣔⠞⣽⣟⠊⠱⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⣤⡶⠗⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⠾⠉⠀⣀⣙⣷⠤⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣬⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠘⠉⠀⠀⣀⠞⠁⠙⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣠⡶⠞⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡶⠊⠀⠀⠀⠘⠓⠶⠴⠴⠦⠦⠦⠶⣄⡬⠭⠓⠊⠁⠀⠀⠀⠀⠀"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            await cmd.reply_text(f"Join [Neko Bots 😼](https://t.me/neko_bots) to access me.\n\n{meow}", reply_markup=dl_markup)


@app.on_message(filters.private & filters.regex("http|https"))
async def Ouo(bot, cmd: Message):
    user = await app.get_chat_member(-1001315223923, cmd.from_user.id)
    usr_cmd = str(cmd.text)
    if user.status == enums.ChatMemberStatus.MEMBER:
        x1 = await cmd.reply_text("`Meow! Bypassing...` 😺")
        url = (usr_cmd).split("_")[-1]
        bl = ouo_bypass(url)
        asyncio.sleep(3)
        await x1.delete()
        x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot.")
    elif user.status == enums.ChatMemberStatus.ADMINISTRATOR:
        x1 = await cmd.reply_text("`Meow! Bypassing...` 😺")
        url = (usr_cmd).split("_")[-1]
        bl = ouo_bypass(url)
        asyncio.sleep(3)
        await x1.delete()
        x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot.")
    elif user.status == enums.ChatMemberStatus.OWNER:
        x1 = await cmd.reply_text("`Meow! Bypassing...` 😺")
        url = (usr_cmd).split("_")[-1]
        bl = ouo_bypass(url)
        asyncio.sleep(3)
        await x1.delete()
        x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot.")

repl_markup=InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        text="🐌TG FILE",

                        url="https://telegram.me/somayukibot?start=animxt_MjQ1Nw==",

                    ),

                    InlineKeyboardButton(

                        text="🚀BETA DL",

                        url="https://da.gd/ll0oCI",

                    ),
  
                ],
                    
            ],
        )
@app.on_message(filters.command("send"))
async def stdart(bot, message: Message):
  sourcetext =  f"**#Encoded_File**" + "\n" + f"**‣ File Name**: `Ikenaikyo - 01 [720p x265] @animxt.mkv`" + "\n" + f"**‣ Video**: `720p HEVC x265 10Bit`" + "\n" + f"**‣ Audio**: `Japanese`" + "\n" + f"**‣ Subtitle**: `English, Portuguese (Brazil), Spanish (Latin America), Spanish, French, German, Italian, Russian`" + "\n" + f"**‣ File Size**: `92 MBs`" + "\n" + f"**‣ Duration:** `24 minutes 42 seconds`" + "\n" + f"**‣ Downloads:** [🔗Telegram File](https://telegram.me/somayukibot?start=animxt_MjQ1Nw==) 🔗[BETA DL](https://da.gd/ll0oCI)"       
  untextx = await app.send_message(
                      chat_id=-1001159872623,
                      text=sourcetext,
                      reply_to_message_id=35196,
                      reply_markup=repl_markup
)            
            
@app.on_message(filters.command("link") & filters.private)

async def link(bot, cmd: Message):
    usr_cmd = cmd.text.split("_", 1)[-1]
    if usr_cmd == "/link":

       await cmd.reply_text("Fuck off!")

    else: 
        try:

       
            fuk_cmd = cmd.text.replace("/link https://t.me/c/1642923224/", "")
            filex_id = str_to_b64(fuk_cmd)
            sendx = await app.send_message(chat_id=cmd.from_user.id, text="https://t.me/somayukibot?start=animxt_" + filex_id)
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `XXXXXXX`")

    
app.start()
print("Powered by @animxt")
idle()
