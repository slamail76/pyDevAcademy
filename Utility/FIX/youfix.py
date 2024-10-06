from pytubefix import YouTube
from pytubefix import Playlist
from pytubefix.cli import on_progress
import re
import ffmpeg
import subprocess
import os

def video_audio_mux(audiosource, videosource, out):
    codec = "copy"
    subprocess.run(f"ffmpeg -i {audiosource} -i {videosource} -c {codec} {out}")

url = "https://www.youtube.com/watch?v=C1mlBijIYWk&list=PLbUoro2CIdD2JMRJnnplItRL6VVjfSIg8&index=1"
yt = YouTube(url, on_progress_callback=on_progress)

n = 1
ys = yt.streams.filter(progressive=False).order_by('resolution').desc() # output of this line is None
#lista = list(ys) #da commentare
#print(type(lista)) # da commentare
#print("\n".join(map(str, lista))) #da commentare
yt.title = (f'{n} {yt.title}')
path = "D:\Download\AI\\"
filevideo = str(path+yt.title+".mp4").replace(" ", "_")
print(filevideo)
print(len(filevideo))

print(filevideo)
yt.title = re.sub("\.", "", yt.title)
stream = yt.streams.get_by_itag(137)
stream.download(output_path='D:\Download\AI', filename= "video.mp4" )

audio = yt.streams.filter(only_audio=True)
listaa = list(audio)
print("\n".join(map(str, listaa)))
streama = yt.streams.get_by_itag(140)
streama.download(output_path='D:\Download\AI', filename= "audio.mp4" )

video = str(path +"video.mp4")
audio2 = str(path +"audio.mp4")

video_audio_mux(audio2,video,filevideo)
os.remove(video)
os.remove(audio2)








