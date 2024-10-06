import yt_dlp

yt_opts = {
    'verbose': True,
    'download_sections': [{
        'section': {
            'start_time': 2,
            'end_time': 7
        }
    }]
}

ydl = yt_dlp.YoutubeDL(yt_opts)

ydl.download("https://www.youtube.com/watch?v=BxUS1K7xu30")