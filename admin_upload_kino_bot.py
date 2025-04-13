
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Ruxsat berilgan admin (send your Telegram user ID here)
ADMIN_ID = 770818868  # Bu yerga o'zingizni Telegram ID'ingizni yozing
VIDEO_FOLDER = "videos"

# Papkani avtomatik yaratish
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# Xabarlarni boshqarish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Agar bu admin bo‘lsa va video yuborgan bo‘lsa
    if update.message.video and user_id == ADMIN_ID:
        caption = update.message.caption

        if caption and caption.isdigit():
            filename = f"{caption}.mp4"
            filepath = os.path.join(VIDEO_FOLDER, filename)
            video_file = await update.message.video.get_file()
            await video_file.download_to_drive(filepath)
            await update.message.reply_text(f"{caption}-raqamli kino saqlandi!")
        else:
            await update.message.reply_text("Iltimos, videoga raqam yozilgan caption qo‘shing.")
    
    # Oddiy foydalanuvchi raqam yuborsa
    elif update.message.text and update.message.text.strip().isdigit():
        code = update.message.text.strip()
        file_path = os.path.join(VIDEO_FOLDER, f"{code}.mp4")

        if os.path.exists(file_path):
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open(file_path, 'rb'))
        else:
            await update.message.reply_text("Kechirasiz, bu kodga mos video topilmadi.")
    
    else:
        await update.message.reply_text("Video yuborish uchun admin bo‘lishingiz kerak yoki raqamli kod yuboring.")

# Bot token
TOKEN = "YOUR_BOT_TOKEN"

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))
app.run_polling()
