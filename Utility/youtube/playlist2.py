from pytube import Playlist
from pytube import YouTube as YT
import time

playlist = Playlist('https://www.youtube.com/playlist?list=PLMEZyDHJojxPndMRFPzCZ1T7RgzlHWBUb')
n = 1
for video in playlist.videos:
    playlist = Playlist('https://www.youtube.com/playlist?list=PLMEZyDHJojxPndMRFPzCZ1T7RgzlHWBUb')
    while True:
        try:
            video.title = video.title
            break
        except:
            print("Failed to get name. Retrying...")
            time.sleep(1)
            playlist = Playlist('https://www.youtube.com/playlist?list=PLMEZyDHJojxPndMRFPzCZ1T7RgzlHWBUb')
            continue
    video.title = (f'{n} {video.title}')
    print(video.title)
    #video = YT(playlist.videos[i], use_oauth=True, allow_oauth_cache=True)
    #stream = video.streams.get_by_itag(140)
    st = video.streams.get_highest_resolution()
    st.download(output_path='D:\Download\Musica')
    if ((n % 2) == 0):
        time.sleep(5)
    if ((n % 5) == 0):
        time.sleep(15)
    n += 1