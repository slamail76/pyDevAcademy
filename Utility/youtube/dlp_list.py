import yt_dlp

def scarica_playlist(url_playlist, cartella_destinazione='/media/stefano/Storage/Scaricati/playlist'):
    opzioni = {
        'outtmpl': f'{cartella_destinazione}/%(playlist_title)s/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'yesplaylist': True,
        'ignoreerrors': True,  # Continua anche se ci sono errori su qualche video
    }

    with yt_dlp.YoutubeDL(opzioni) as ydl:
        ydl.download([url_playlist])

if __name__ == "__main__":
    # Inserisci qui l'URL della playlist
    link_playlist = "https://www.youtube.com/playlist?list=PLYtHoWz0tONsBorKxQNcRCUoeWj8Ze7wp"
    scarica_playlist(link_playlist)