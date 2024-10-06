from pytube import Playlist
import re
p = Playlist('https://www.youtube.com/playlist?list=PLWpZilv2DGmQlhLuN9emg7koEXtzNU13l')

print(f'Downloading: {p.title}')
n = 1

for video in p.videos:
    video.title = (f'{n} {video.title}')
    print(video.title)
    video.title = re.sub("\.", "", video.title)
    st = video.streams.get_highest_resolution()
    st.download(output_path='D:\Download\FulvioCorno\BHD-21_22a')
    n += 1



