from pytube import Playlist
from pytube import YouTube as YT
import time

playlist = Playlist('https://www.youtube.com/playlist?list=PLbUoro2CIdD34pJh24APLfdbLShnYUDKK')
n = 1
for video in playlist.videos:
    playlist = Playlist('https://www.youtube.com/playlist?list=PLbUoro2CIdD34pJh24APLfdbLShnYUDKK')
    while True:
        try:
            video.title = video.title
            break
        except:
            print("Failed to get name. Retrying...")
            time.sleep(5)
            playlist = Playlist('https://www.youtube.com/playlist?list=PLbUoro2CIdD34pJh24APLfdbLShnYUDKK')
            continue
    video.title = (f'{n} {video.title}')
    print(video.title)