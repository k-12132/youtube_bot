import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل /download <رابط_يوتيوب> لتحميل الفيديو 🎥")

# أمر التحميل
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ رجاءً ارسل رابط يوتيوب بعد الأمر.\nمثال: /download https://youtu.be/xyz")
        return

    url = context.args[0]
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

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))
    app.run_polling()

if __name__ == "__main__":
    main()
