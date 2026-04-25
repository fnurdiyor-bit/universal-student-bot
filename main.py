import logging
import os  # Buni qo'shdik
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask  # Render botni o'chirib qo'ymasligi uchun kerak

# Render botni o'chirib qo'ymasligi uchun kichik veb-server yaratamiz
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# ASOSIY MA'LUMOTLAR
API_TOKEN = '8690723618:AAH0rdjT7t96JELflhipuL0Xa54J1QKqphI'
MY_CARD = '5614683514401090'
OWNER_NAME = 'Nurdiyor Fayzullayev'
MY_USERNAME = 'Nurdiyor_0107'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    btn_music = InlineKeyboardButton("🎵 Musiqa/Video yuklash", callback_data='music')
    btn_orders = InlineKeyboardButton("💻 Slayd & Referat", callback_data='orders')
    markup.add(btn_music, btn_orders)

    welcome_text = (
        f"Salom, {message.from_user.first_name}! 👋\n\n"
        "Bu bot orqali musiqa yuklashingiz yoki sifatli slaydlar buyurtma qilishingiz mumkin.\n\n"
        "Kerakli bo'limni tanlang 👇"
    )
    await message.answer(welcome_text, reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'orders')
async def show_prices(callback_query: types.CallbackQuery):
    price_text = (
        "💰 **Xizmatlarimiz narxi:**\n\n"
        "💻 1 ta slayd — 2 000 so'm\n"
        "📝 Referat — 10 000 so'mdan\n"
        "📑 Kurs ishi — Kelishilgan narxda\n\n"
        "🎁 **BONUS:** Birinchi buyurtmangizda 1 ta slayd tekin!\n\n"
        f"💳 **To'lov uchun karta:** `{MY_CARD}`\n"
        f"👤 **Egasi:** {OWNER_NAME}\n\n"
        f"Buyurtma berish uchun adminga yozing: @{MY_USERNAME}\n"
        "*(To'lov qilgach, chekni rasmga olib yuboring!)*"
    )
    await bot.send_message(callback_query.from_user.id, price_text, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'music')
async def music_info(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Musiqa yoki Video yuklash uchun YouTube/Instagram linkini yuboring... 📥")

@dp.message_handler()
async def handle_all(message: types.Message):
    if 'http' in message.text:
        await message.answer("Sizning so'rovingiz qabul qilindi. Tez orada yuklab beriladi... ⏳")
    else:
        await message.answer("Iltimos, pastdagi menyudan foydalaning yoki link yuboring.")

if __name__ == '__main__':
    # Render uchun maxsus: veb-serverni alohida oqimda yurgizamiz yoki shunchaki polling qilamiz
    # Lekin eng muhimi: Render port kutadi.
    executor.start_polling(dp, skip_updates=True)
