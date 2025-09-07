from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os
import asyncio

# =======================
# إعدادات أساسية
# =======================
TELEGRAM_TOKEN = "ضع_توكن_البوت_هنا"  # ضع توكن البوت
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# =======================
# FastAPI
# =======================
app = FastAPI()

@app.post("/download")
async def api_download(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return {"status": "error", "message": "يرجى إدخال رابط الفيديو"}

    filename = await download_video(url)
    return {"status": "success", "file": filename}

# =======================
# yt-dlp تحميل الفيديو
# =======================
async def download_video(url):
    ydl_opts = {"outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")}
    loop = asyncio.get_event_loop()
    try:
        info = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=True))
        return yt_dlp.YoutubeDL(ydl_opts).prepare_filename(info)
    except Exception as e:
        return str(e)

# =======================
# Telegram Bot
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرسل رابط الفيديو لتحميله.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("جاري تحميل الفيديو... ⏳")
    filename = await download_video(url)
    if os.path.exists(filename):
        await update.message.reply_document(document=open(filename, "rb"))
        await msg.edit_text("تم التحميل بنجاح ✅")
    else:
        await msg.edit_text(f"حدث خطأ: {filename}")

def run_bot():
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app_bot.run_polling()

# =======================
# تشغيل البوت و FastAPI معاً
# =======================
if __name__ == "__main__":
    import threading
    import uvicorn

    # تشغيل البوت في thread منفصل
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # تشغيل FastAPI
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
