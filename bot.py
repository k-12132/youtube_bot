import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

BOT_TOKEN = "ضع_توكن_البوت_هنا"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرسل لي رابط الفيديو لتحميله.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    # مسار حفظ الفيديو مؤقتاً
    output_path = "downloaded_video.mp4"

    ydl_opts = {
        "outtmpl": output_path,
        "format": "best",
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # إرسال الفيديو للمستخدم
        with open(output_path, "rb") as video:
            await update.message.reply_video(video)
        os.remove(output_path)  # حذف الملف بعد الإرسال
    except Exception as e:
        await update.message.reply_text(f"❌ لا يمكن تحميل هذا الفيديو.\nالخطأ: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    app.run_polling()  # يمكنك تغييرها لاحقاً إلى webhook إذا أردت

if __name__ == "__main__":
    main()
