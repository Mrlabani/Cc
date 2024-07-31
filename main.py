import pyrogram
from pyrogram import Client, filters
import re
import asyncio
import aiohttp
import logging
import os

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def correct_padding(session_string):
    """Ensure session string has correct padding."""
    return session_string + "=" * ((4 - len(session_string) % 4) % 4)

# Load environment variables
API_ID = os.getenv('23445865')
API_HASH = os.getenv('350af94c05757b670d2a3825975da0b3')
SESSION_STRING = correct_padding(os.getenv('BAFlwWkAxE_BmPxHkU6hLf2vSpEHoMzxJq6PIg7BXKXefzbApNY4lqT22UX88XMNngbMFG1utXiqINSi_QtnzQNOI3QNdArOKjIwQRcU2PgCcgcyV9iIUoWgyKAxZRCN7SCpgdau2Q-VbRJKnfTgtJDkqc4Efk8GO9mDR-e-TTRicL-NRNbJs8TU6gkt44Hj9UGojnrTqOGqcP9KdYuo0dh8Sp004eqgmPBnNuoHut2wreOG_n8joQhMYBdmtMT7E9nXiKHvlcaTdspM6DB6BmIvMjW3j37BG6yikQN0QBV8JLhNeXZyptDTWuCyw-a3H-XLkw7VBrTjHxLGPucfx1UIwDroBAAAAAGB25UeAA'))

app = pyrogram.Client(
    'noob_scrapper',
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

BIN_API_URL = 'https://astroboyapi.com/api/bin.php?bin={}'
RATE_LIMIT = 1  # Rate limit in seconds

def filter_cards(text):
    """Extract card information using regex."""
    regex = r'\d{15,16}\D*\d{2}\D*\d{2,4}\D*\d{3,4}'
    return re.findall(regex, text)

async def bin_lookup(bin_number):
    """Fetch BIN information from the API."""
    bin_info_url = BIN_API_URL.format(bin_number)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        try:
            async with session.get(bin_info_url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"BIN API returned status {response.status} for BIN {bin_number}")
                    return None
        except aiohttp.ClientError as e:
            logger.error(f"Aiohttp ClientError: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during bin lookup: {e}")
            return None

async def rate_limited_bin_lookup(bin_number):
    """Perform BIN lookup with rate limiting."""
    await asyncio.sleep(RATE_LIMIT)
    return await bin_lookup(bin_number)

def validate_bin_info(bin_info):
    """Validate BIN information fields."""
    required_fields = ["brand", "type", "level", "bank", "country_name", "country_flag"]
    return all(field in bin_info for field in required_fields)

async def approved(client_instance, message):
    """Process approved messages and send formatted responses."""
    try:
        if re.search(r'(Approved!|Charged|authenticate_successful|𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱|APPROVED|New Cards Found By NoobScrapper|ꕥ Extrap [☭]|み CVV CCN 2D SCRAPE by|Approved) ✅', message.text):
            filtered_card_info = filter_cards(message.text)
            if not filtered_card_info:
                return

            for card_info in filtered_card_info:
                bin_number = card_info[:6]
                bin_info = await rate_limited_bin_lookup(bin_number)
                if bin_info and validate_bin_info(bin_info):
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
                        f"**𝖢𝖮𝖴𝖭𝖳𝖲** ➠ <b>{country}, {country_flag}</b>\n\n"
                        "**𝖢𝖱𝖤𝖠𝖳𝖮𝖱** ➠ <b>๏─NOOB─๏</b>"
                    )

                    await client_instance.send_message(chat_id='-1002168161975', text=formatted_message)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

@app.on_message(filters.text)
async def astro(client_instance, message):
    """Handle incoming messages."""
    if message.text:
        await approved(client_instance, message)

if __name__ == "__main__":
    app.run()
