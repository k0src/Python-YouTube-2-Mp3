import tkinter as tk
import ttkbootstrap as ttk
from pytube import YouTube 
import os
from tkinter import filedialog
from PIL import Image, ImageTk
import urllib.request
import io

photo = None

def download():
    global photo

    directory_path = filedialog.askdirectory()

    if not directory_path:
        return
    
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

    video_label_var.set(yt.title)

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

title = ttk.Label(window, text="YouTube To Mp3", font = 'Calibri 24 bold')
title.pack(pady=5)

subtitle2 = ttk.Label(window, text="Paste a YouTube Link:", font = 'Calibri 18')
subtitle2.pack(pady=5)

download_string = tk.StringVar()
download_entry = ttk.Entry(window, textvariable=download_string, width=50)
download_entry.pack(pady=5)
download_button = ttk.Button(window, text='Download', command=download)
download_button.pack(pady=5)


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