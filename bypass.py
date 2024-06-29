import asyncio
import os
import re
from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from base64 import standard_b64encode, standard_b64decode
from pyrogram import Client, filters, idle, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import logging
from db import add_user, full_userbase, present_user, del_user
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)




logging.getLogger("pyrogram").setLevel(logging.WARNING)
app = Client(
            "Bot",
            bot_token = "7459878689:AAGA92Ifi5gilBaNOGtfiacv3ZirFnpnI3M",
            api_id = 10247139,
            api_hash = "96b46175824223a33737657ab943fd6a")


# ouo url
# Examples:
# https://ouo.io/HxFVfD - ouo.io links (no account -> only one step)
# https://ouo.press/Zu7Vs5 - ouo.io links (with account -> two steps)
# Can exchange between ouo.press and ouo.io


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
    'authority': 'ouo.press',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'referer': 'http://www.google.com/ig/adde?moduleurl=',
    'upgrade-insecure-requests': '1',
})

# -------------------------------------------
# OUO BYPASS


def ouo_bypass(url):
    tempurl = url.replace("ouo.io", "ouo.press")
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

@app.on_message(filters.command("start") & filters.private)
async def start(bot, cmd: Message):
    usr_cmd = cmd.text.split("_", 1)[-1]
    kay_id = -1001642923224
    id = cmd.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    if usr_cmd == "/start":
        await cmd.reply_text("""**Meow! Send me "ouo.io" or "ouo.press" link & I'll bypass & send you the destination link. 😺**""")
    else:
        try:
            user = await app.get_chat_member(-1001315223923, cmd.from_user.id)
            if user.status == enums.ChatMemberStatus.MEMBER:
                x1 = await cmd.reply_text("`Meow! Bypassing...` 😺\n\n")
                url = (usr_cmd).split("_")[-1]
                b = ouo_bypass(url)
                bl = b['bypassed_link']
                asyncio.sleep(3)
                await x1.delete()
                x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot. /ᐠ. ｡.ᐟ\ᵐᵉᵒʷˎˊ˗")
            elif user.status == enums.ChatMemberStatus.ADMINISTRATOR:
                x1 = await cmd.reply_text("`Meow! Bypassing...` 😺")
                url = (usr_cmd).split("_")[-1]
                b = ouo_bypass(url)
                bl = b['bypassed_link']
                asyncio.sleep(3)
                await x1.delete()
                x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot.")
            elif user.status == enums.ChatMemberStatus.OWNER:
                x1 = await cmd.reply_text("`Meow! Bypassing...` 😺")
                url = (usr_cmd).split("_")[-1]
                b = ouo_bypass(url)
                bl = b['bypassed_link']
                asyncio.sleep(3)
                await x1.delete()
                x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot. /ᐠ. ｡.ᐟ\ᵐᵉᵒʷˎˊ˗")
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
                await cmd.reply_text(f"Join [Neko Bots 😼](https://t.me/neko_bots) to access me.", reply_markup=dl_markup)
        except Exception as err:
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
            await cmd.reply_text(f"Join [Neko Bots 😼](https://t.me/neko_bots) to access me.", reply_markup=dl_markup)


@app.on_message(filters.private & filters.regex("http|https"))
async def Ouo(bot, cmd: Message):
    user = await app.get_chat_member(-1001315223923, cmd.from_user.id)
    usr_cmd = str(cmd.text)
    if user.status == enums.ChatMemberStatus.MEMBER:
        x1 = await cmd.reply_text("`Meow! Bypassing...` 😺")
        url = usr_cmd
        b = ouo_bypass(url)
        bl = b['bypassed_link']
        asyncio.sleep(3)
        await x1.delete()
        x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot. /ᐠ. ｡.ᐟ\ᵐᵉᵒʷˎˊ˗")
    elif user.status == enums.ChatMemberStatus.ADMINISTRATOR:
        x1 = await cmd.reply_text("`Meow! Bypassing...` 😺")
        url = usr_cmd
        b = ouo_bypass(url)
        bl = b['bypassed_link']
        asyncio.sleep(3)
        await x1.delete()
        x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot. /ᐠ. ｡.ᐟ\ᵐᵉᵒʷˎˊ˗")
    elif user.status == enums.ChatMemberStatus.OWNER:
        x1 = await cmd.reply_text("`Meow! Bypassing...` 😺")
        url = usr_cmd
        b = ouo_bypass(url)
        bl = b['bypassed_link']
        asyncio.sleep(3)
        await x1.delete()
        x2 = await cmd.reply_text(f"**Original Link:** `{url}`\n\n**Destination Link:** `{bl}`\n\nThank you! for using @ouo_bypass_robot. /ᐠ. ｡.ᐟ\ᵐᵉᵒʷˎˊ˗")

@app.on_message(filters.command('users') & filters.private & filters.user(1443454117))
async def get_users(bot, message: Message):
    msg = await app.send_message(chat_id=message.chat.id, text="`Fetching`")
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@app.on_message(filters.private & filters.command('broadcast') & filters.user(1443454117))
async def send_text(bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
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
