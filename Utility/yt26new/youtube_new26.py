from yt_dlp import YoutubeDL

url = input("URL YouTube: ").strip()

ydl_opts = {
    "format": "bv*+ba/b",
    "outtmpl": "%(title)s.%(ext)s",
    "merge_output_format": "mp4",
    "noplaylist": True,
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download completato.")