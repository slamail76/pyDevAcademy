# importing the module

from pytube import YouTube

link = ".mp4"

yt = YouTube(link)

try:

    yt.streams.filter(progressive = True,
    file_extension = "mp4").first().download(output_path = "D:\Download\math1",
    filename = "Numeri naturali #2 - Proprietà delle operazioni e delle potenze. Criteri di Divisibilità.mp4")

except:
    print("Some Error!")
print('Task Completed!')