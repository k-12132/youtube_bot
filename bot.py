import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Regex للتأكد من أن النص هو رابط يوتيوب
YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط يوتيوب مباشرة أو استخدم الأمر:\n/download <رابط> 🎥")

# وظيفة التحميل
async def handle_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    try:
        # تحميل الفيديو
        ydl_opts = {
            "outtmpl": "video.mp4",
            "format": "mp4/best"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # إرسال الفيديو
        with open("video.mp4", "rb") as f:
            await update.message.reply_video(f)

        os.remove("video.mp4")

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التحميل: {e}")

# أمر /download
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ رجاءً ارسل رابط يوتيوب بعد الأمر.\nمثال: /download https://youtu.be/xyz")
        return
    url = context.args[0]
    await handle_youtube(update, context, url)

# عند إرسال أي رسالة نصية (نبحث إذا كانت رابط يوتيوب)
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if re.match(YOUTUBE_REGEX, text):
        await handle_youtube(update, context, text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))

    # أي رسالة نصية فيها رابط يوتيوب
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))

    app.run_polling()

if __name__ == "__main__":
    main()
