import yt_dlp

def scarica_playlist(url, cartella_destinazione='/media/stefano/Storage/Scaricati/playlist'):
    opzioni = {
        'outtmpl': f'{cartella_destinazione}/%(playlist_title)s/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'yesplaylist': True,
    }

    with yt_dlp.YoutubeDL(opzioni) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    link = "https://www.youtube.com/watch?v=BxUS1K7xu30"
    scarica_playlist(link)