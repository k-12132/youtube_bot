import http.client
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# إعداد البوت
BOT_TOKEN = "ضع_توكن_البوت_هنا"

# دالة لجلب الفيديوهات من RapidAPI
def get_playlist_videos(playlist_id):
    conn = http.client.HTTPSConnection("youtube-media-downloader.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "e063166858msh759b8dd68f14471p1c86c8jsnc333e7700feb",
        'x-rapidapi-host': "youtube-media-downloader.p.rapidapi.com"
    }

    conn.request("GET", f"/v2/playlist/videos?playlistId={playlist_id}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    videos = json.loads(data.decode("utf-8"))
    return videos.get("videos", [])

# دالة البوت لإرسال الفيديوهات
async def playlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    playlist_id = "PLeCdlPO-XhWFzEVynMsmosfdRsIZXhZi0"  # ضع هنا أي قائمة تشغيل
    videos = get_playlist_videos(playlist_id)
    
    if not videos:
        await update.message.reply_text("لم يتم العثور على فيديوهات في هذه القائمة.")
        return
    
    for video in videos:
        title = video.get("title")
        url = video.get("url")
        await update.message.reply_text(f"{title}\n{url}")

# إعداد التطبيق وتشغيل البوت
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("playlist", playlist))

if __name__ == "__main__":
    print("البوت يعمل...")
    app.run_polling()
