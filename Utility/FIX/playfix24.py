from pytubefix import YouTube
from pytubefix import Playlist
from pytubefix.cli import on_progress
import re
import subprocess
import os

def video_audio_mux(audiosource, videosource, out):
    codec = "copy"
    subprocess.run(f"ffmpeg -i {audiosource} -i {videosource} -c {codec} {out}")

url = "https://www.youtube.com/watch?v=4OUUK1VgeQU&list=PLFMns86uumjjX0zHm2hzKi_Yr18YzV5qr"
path = "D:\Download\Musica\ickelback\\"

pl = Playlist(url)

n = 1
for videofor in pl.videos:
    ys = videofor.streams.filter(progressive=False).order_by('resolution').desc() # output of this line is None
    videofor.title = (f'{n} {videofor.title}')
    videofor.title = re.sub("\.", "", videofor.title)
    filevideo = str(path+videofor.title+".mp4").replace(" ", "_")
    print(filevideo)

    stream = videofor.streams.get_by_itag(137)
    stream.download(output_path=path, filename= "video.mp4" )

    audio = videofor.streams.filter(only_audio=True)
    streama = videofor.streams.get_by_itag(140)
    streama.download(output_path=path, filename= "audio.mp4" )

    audio2 = str(path + "audio.mp4")
    video = str(path + "video.mp4")
    n = n + 1

    video_audio_mux(audio2,video,filevideo)
    os.remove(video)
    os.remove(audio2)
