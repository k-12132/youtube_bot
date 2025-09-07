import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# جلب التوكن من Render Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# بيانات Webhook
PORT = int(os.environ.get("PORT", 8443))
HOST = "0.0.0.0"
WEBHOOK_URL = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{BOT_TOKEN}"

# Regex لرابط يوتيوب
YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أرسل لي أي رابط يوتيوب وسأقوم بتحميله لك 🎥")

# تحميل فيديو من يوتيوب
async def handle_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    try:
        ydl_opts = {
            "outtmpl": "video.mp4",
            "format": "mp4/best"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open("video.mp4", "rb") as f:
            await update.message.reply_video(f)

        os.remove("video.mp4")

    except Exception as e:
        await update.message.reply_text(f"❌ خطأ أثناء التحميل: {e}")

# أمر /download
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ استخدم الأمر هكذا:\n/download https://youtu.be/xxxx")
        return
    url = context.args[0]
    await handle_youtube(update, context, url)

# التحقق من أي رسالة نصية (إذا كانت رابط يوتيوب)
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if re.match(YOUTUBE_REGEX, text):
        await handle_youtube(update, context, text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))

    # تشغيل Webhook في Render
    app.run_webhook(
        listen=HOST,
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
