# importing the module

from pytube import YouTube

link = "https://www.youtube.com/watch?v=7jfRG-fgvQ8"

yt = YouTube(link)

try:

    yt.streams.filter(progressive = True,
    file_extension = "mp4").first().download(output_path = "D:\Download",
    filename = "Enya.mp4")

except:
    print("Some Error!")
print('Task Completed!')