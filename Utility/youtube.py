# importing the module

from pytube import YouTube

link = "https://www.youtube.com/watch?v=yYdC9ieX3SE"

yt = YouTube(link)

try:

    yt.streams.filter(progressive = True,
    file_extension = "mp3").first().download(output_path = "D:\Download", filename = "Deep.mp3")


except:
    print("Some Error!")
print('Task Completed!')