import tkinter as tk
import ttkbootstrap as ttk
from pytube import YouTube, Playlist
import os
from tkinter import filedialog
from PIL import Image, ImageTk
import urllib.request
import io

photo = None

def download():
    global photo

    if 'youtube.com' not in str(download_string.get()) and 'youtu.be' not in str(download_string.get()):
        error_message.set(f'{download_string.get()} is not a valid YouTube URL!')
        return
    
    directory_path = filedialog.askdirectory()

    if not directory_path:
        return
    
    if ',' in str(download_string.get()):
        urls = str(download_string.get()).split(',')

        for url in urls:
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=directory_path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
        
        if batch_thumbs_option_var.get() == 1:
            for url in urls:
                yt = YouTube(url)
                with urllib.request.urlopen(yt.thumbnail_url) as u:
                    raw_data = u.read()
                image = Image.open(io.BytesIO(raw_data))
                image.save(f"{directory_path}/{yt.title}.jpg")

    elif 'list=' in str(download_string.get()):
        yt = Playlist(str(download_string.get()))

        for video in yt.videos:
            video = video.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=directory_path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

        if batch_thumbs_option_var.get() == 1:
            for video in yt.videos:
                with urllib.request.urlopen(video.thumbnail_url) as u:
                    raw_data = u.read()
                image = Image.open(io.BytesIO(raw_data))
                image.save(f"{directory_path}/{video.title}.jpg")

    else:
        yt = YouTube(str(download_string.get()))

        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=directory_path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        with urllib.request.urlopen(yt.thumbnail_url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        photo = ImageTk.PhotoImage(image)

        video_label_var.set(f'{yt.title} - {yt.author}')

        video_thumb.config(image=photo)

        download_thumb_button['state'] = tk.NORMAL

def download_thumb():
    directory_path = filedialog.askdirectory()

    if not directory_path:
        return

    yt = YouTube(str(download_string.get()))

    with urllib.request.urlopen(yt.thumbnail_url) as u:
        raw_data = u.read()
    image = Image.open(io.BytesIO(raw_data))
    image.save(f"{directory_path}/{yt.title}.jpg")

window = ttk.Window(themename="darkly")
window.title("PyDownloader")
window.geometry('1000x780')
window.maxsize(1000, 780)
window.minsize(1000, 780)

video_label_var = tk.StringVar()
error_message = tk.StringVar()

title = ttk.Label(window, text="YouTube To Mp3", font = 'Calibri 24 bold')
title.pack(pady=5)

subtitle2 = ttk.Label(window, text='Paste a YouTube Video or Playlist Link (or multiple videos seperated with ","):', font = 'Calibri 16')
subtitle2.pack(pady=5)

download_string = tk.StringVar()
download_entry = ttk.Entry(window, textvariable=download_string, width=50)
download_entry.pack(pady=5)
error_label = ttk.Label(window, text='', textvariable=error_message, font='Calibri 14', foreground='red')
error_label.pack(pady=5)
download_button = ttk.Button(window, text='Download', command=download)
download_button.pack(pady=5)

batch_thumbs_option_var = tk.IntVar(value=0)

batch_thumbs_option = ttk.Checkbutton(window, text='Batch Download Thumbnails', variable = batch_thumbs_option_var, onvalue=1, offvalue=0)
batch_thumbs_option.pack(pady=5)


video_thumb_label = ttk.Label(window, text="Video Thumbnail:", font='Calibri 18')
video_thumb_label.pack(pady=5)

video_thumb = ttk.Label(window)
video_thumb.pack(pady=5)

video_label = ttk.Label(window, textvariable=video_label_var, font='Calibri 18')
video_label.pack(pady=5)

download_thumb_button = ttk.Button(window, text='Download Thumbnail', command=download_thumb)
download_thumb_button.pack(pady=5)
download_thumb_button['state'] = tk.DISABLED

window.mainloop()