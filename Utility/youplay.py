from pytube import Playlist
import re
p = Playlist('https://www.youtube.com/playlist?list=PLqRTLlwsxDL_O2e73lHQvJyucwpcMQUnO')

print(f'Downloading: {p.title}')
n = 1

for video in p.videos:
    video.title = (f'{n} {video.title}')
    print(video.title)
    #video.title = re.sub("\.", "", video.title)
    st = video.streams.get_highest_resolution()
    st.download(output_path='D:\Download\FulvioCorno\BHD-21_22')
    n += 1

   # try:
   #     st = video.streams.get_highest_resolution()
   #     st.download(output_path = 'D:\Download\FulvioCorno\BHD-20_21')
   # except:
   #     continue
   # n += 1


