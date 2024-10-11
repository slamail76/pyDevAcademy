from pytubefix import YouTube
from pytubefix.cli import on_progress

url = "https://www.youtube.com/watch?v=xfVWsLxCcuQ&list=PLbXZkxjs1XprPY04zKSF6ADTEPF0J54jC"
path = "D:\Download\Musica\\"

yt = YouTube(url, on_progress_callback = on_progress)
print(yt.title)

ys = yt.streams.filter(progressive=False).order_by('resolution').desc()
audio = yt.streams.filter(only_audio=True)
lista = list(audio)
print(type(lista))
print("\n".join(map(str, lista)))


ys = yt.streams.get_by_itag(140)
#ys = yt.streams.get_audio_only()
ys.download(mp3=True, output_path=path, filename= "gamma25.mp3")