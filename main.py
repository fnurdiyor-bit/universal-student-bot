import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from yt_dlp import YoutubeDL

# --- SOZLAMALAR ---
# DIQQAT: Pastdagi ma'lumotlarni o'zingniki bilan almashtir!
API_TOKEN = 'TOKENINGNI_SHUYERGA_YOZ' 
CHANNEL_ID = '@KANALINGNI_YOZ' 
ADMIN_USER = '@USERNAMINGNI_YOZ' 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- TUGMALAR ---
glavny_menu = ReplyKeyboardMarkup(resize_keyboard=True)
glavny_menu.add(KeyboardButton("📥 Video yuklash"), KeyboardButton("🎓 Talaba bo'limi"))

student_menu = ReplyKeyboardMarkup(resize_keyboard=True)
student_menu.add("💻 Slayd tayyorlash", "📚 Referat yozish")
student_menu.add("📝 Kurs ishi", "⬅️ Orqaga")

# --- FUNKSIYALAR ---
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status != 'left'
    except: return True

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"Xush kelibsiz!\n\nBotdan foydalanish uchun {CHANNEL_ID} kanaliga a'zo bo'ling.", reply_markup=glavny_menu)

@dp.message_handler(lambda m: m.text == "🎓 Talaba bo'limi")
async def student(message: types.Message):
    await message.answer("Xizmatni tanlang:", reply_markup=student_menu)

@dp.message_handler(lambda m: m.text == "⬅️ Orqaga")
async def back(message: types.Message):
    await message.answer("Asosiy menyu:", reply_markup=glavny_menu)

@dp.message_handler(lambda m: m.text in ["💻 Slayd tayyorlash", "📚 Referat yozish", "📝 Kurs ishi"])
async def services(message: types.Message):
    await message.answer(f"Siz {message.text} bo'limini tanladingiz.\n\nBuyurtma berish uchun adminga yozing: {ADMIN_USER}")

@dp.message_handler()
async def download(message: types.Message):
    if not await check_sub(message.from_user.id):
        await message.answer(f"Avval kanalga a'zo bo'ling: {CHANNEL_ID}")
        return

    url = message.text
    if any(x in url for x in ["instagram.com", "tiktok.com", "youtube.com", "youtu.be"]):
        msg = await message.answer("🚀 Video tahlil qilinmoqda...")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': 'v.mp4', 'max_filesize': 45*1024*1024}
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open('v.mp4', 'rb') as video:
                await bot.send_video(message.chat.id, video, caption="✅ Yuklab olindi!")
            os.remove('v.mp4')
            await msg.delete()
        except:
            await msg.edit_text("❌ Xato! Link noto'g'ri yoki video juda katta.")
    else:
        if message.text != "📥 Video yuklash":
            await message.answer("Iltimos, video linkini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

