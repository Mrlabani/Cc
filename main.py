from flask import Flask
import pyrogram
from pyrogram import Client, filters
import re
import asyncio
import aiohttp
import os

app = Flask(__name__)

def correct_padding(session_string):
    return session_string + "=" * ((4 - len(session_string) % 4) % 4)

# Replace these values with your actual API ID, API hash, and session string
API_ID = os.getenv('23445865')
API_HASH = os.getenv('350af94c05757b670d2a3825975da0b3')
SESSION_STRING = correct_padding(os.getenv('BAFlwWkAxE_BmPxHkU6hLf2vSpEHoMzxJq6PIg7BXKXefzbApNY4lqT22UX88XMNngbMFG1utXiqINSi_QtnzQNOI3QNdArOKjIwQRcU2PgCcgcyV9iIUoWgyKAxZRCN7SCpgdau2Q-VbRJKnfTgtJDkqc4Efk8GO9mDR-e-TTRicL-NRNbJs8TU6gkt44Hj9UGojnrTqOGqcP9KdYuo0dh8Sp004eqgmPBnNuoHut2wreOG_n8joQhMYBdmtMT7E9nXiKHvlcaTdspM6DB6BmIvMjW3j37BG6yikQN0QBV8JLhNeXZyptDTWuCyw-a3H-XLkw7VBrTjHxLGPucfx1UIwDroBAAAAAGB25UeAA'))

client = pyrogram.Client(
    'noob_scrapper',
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

BIN_API_URL = 'https://astroboyapi.com/api/bin.php?bin={}'

def filter_cards(text):
    regex = r'\d{15,16}\D*\d{2}\D*\d{2,4}\D*\d{3,4}'
    matches = re.findall(regex, text)
    return matches

async def bin_lookup(bin_number):
    bin_info_url = BIN_API_URL.format(bin_number)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(bin_info_url) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    return bin_info
                except aiohttp.ContentTypeError:
                    return None
            else:
                return None

async def approved(client_instance, message):
    try:
        if re.search(r'(Approved!|Charged|authenticate_successful|𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱|APPROVED|New Cards Found By NoobScrapper|ꕥ Extrap [☭]|み CVV CCN 2D SCRAPE by|Approved) ✅', message.text):
            filtered_card_info = filter_cards(message.text)
            if not filtered_card_info:
                return

            for card_info in filtered_card_info:
                bin_number = card_info[:6]
                bin_info = await bin_lookup(bin_number)
                if bin_info:
                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")

                    formatted_message = (
                        "┏━━━━━━━⍟\n"
                        "┃**#APPROVED 𝟓$ ✅**\n"
                        "┗━━━━━━━━━━━⊛\n\n"
                        f"**𝖢𝖠𝖱𝖳** ➠ <code>{card_info}</code>\n\n"
                        f"**𝖲𝖳𝖠𝖳𝖴𝖲** ➠ <b>**APPROVED**! ✅</b>\n\n"
                        f"**𝖡𝖨𝖭** ➠ <b>{brand}, {card_type}, {level}</b>\n\n"
                        f"**𝖡𝖠𝖭𝖪** ➠ <b>{bank}</b>\n\n"
                        f"**𝖢𝖮𝖴𝖭𝖳𝖸** ➠ <b>{country}, {country_flag}</b>\n\n"
                        "**𝖢𝖱𝖤𝖠𝖳𝖮𝖱** ➠ <b>๏─𝐍𝐎𝐎𝐁─๏</b>"
                    )

                    await client_instance.send_message(chat_id='-1002160657679', text=formatted_message)
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/')
def index():
    return "Bot is running."

@app.before_first_request
async def start_bot():
    await client.start()

@app.before_first_request
def start_flask():
    client.run()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
  
