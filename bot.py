import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,          # لمنع تحميل قوائم التشغيل
        'ignoreerrors': True,        # تجاهل الأخطاء بدل التعطل
        'quiet': True,               # يقلل الرسائل في الكونسول
        'outtmpl': '%(title)s.%(ext)s',  # حفظ باسم الفيديو
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)  # فقط استخراج المعلومات أولاً
            if info is None:
                return "❌ لا يمكن تحميل هذا الفيديو."
            ydl.download([url])
            return f"✅ تم تحميل الفيديو: {info.get('title')}"
    except Exception as e:
        return f"❌ خطأ أثناء التحميل: {str(e)}"

# مثال على الاستخدام
url = "رابط الفيديو هنا"
result = download_video(url)
print(result)
