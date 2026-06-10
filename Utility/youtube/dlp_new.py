import yt_dlp
import os


def download_media(url, destination_path='downloads', download_type='video'):
    # Ensure destination directory exists
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    if download_type == 'audio':
        # Options for downloading best audio and converting to mp3
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{destination_path}/%(title)s.%(ext)s',
            'noplaylist': True,
            'verbose': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        # Options for downloading best video and audio and merging them
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Select best video and best audio
            'merge_output_format': 'mp4',  # Merge them into an mp4 container
            'outtmpl': f'{destination_path}/%(title)s.%(ext)s',  # Save to specific folder
            'noplaylist': True,  # Ensure we only download the single video
            'verbose': True  # Print detailed log
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Successfully downloaded: {url} to {destination_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


if __name__ == "__main__":
    # Example URL
    video_url = ("https://www.youtube.com/watch?v=5EhGDTaQk0c&list=PLhDjeN9A8LwKg1iWkPKzgeVvhj2sA0cwx&index=1")
    # Define where you want to save the file
    output_folder = r"D:\Download"

    print("Seleziona il tipo di download:")
    print("1. Solo Audio (MP3)")
    print("2. Video e Audio (MP4)")
    choice = input("Scelta (1/2): ")

    mode = 'audio' if choice.strip() == '1' else 'video'

    download_media(video_url, output_folder, mode)