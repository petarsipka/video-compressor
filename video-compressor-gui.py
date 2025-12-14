import ffmpeg
import os
import sys
import tkinter as tk
from tkinter import filedialog
import ctypes
import threading

VIDEO_EXTENSIONS = ('.3g2', '.3gp', '.asf', '.asx', '.avi', '.flv', '.m2ts', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv')

root = tk.Tk()

def find_video(folderpath, output_root):
    for root_dir, _, files in os.walk(folderpath):
        for file in files:
            if file.lower().endswith(VIDEO_EXTENSIONS):
                compress_video(os.path.join(root_dir, file), folderpath, output_root)

def compress_video(filepath, relpath, output_root):
    relative_path = os.path.relpath(filepath, relpath)
    output_path = os.path.join(output_root, relative_path)

    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    print("INPUT :", filepath)
    print("OUTPUT:", output_path)

    ffmpeg.input(filepath).output(
        output_path,
        vcodec="libx264",
        crf=40,
        preset="fast",
        acodec="aac",
        audio_bitrate="96k"
    ).run(overwrite_output=True)


def main():
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
    
    root.title("Video compressor")
    root.geometry("600x500") 
    label = tk.Label(root, text="Select a root folder with videos", font=("Arial", 18))
    label.pack(pady=20) 

    button = tk.Button(root, text="Select folders", font=("Arial", 16), command = on_button_click)
    button.pack(pady=10)
    

    root.mainloop()

def on_button_click():
    folder_path = filedialog.askdirectory(title="Select a root folder")
    if not folder_path:
        return
    
    destination_path = filedialog.askdirectory(title="Select destination folder")
    if not destination_path:
        return
    
    label_source = tk.Label(root, text=f"Source folder: {folder_path}", font=("Arial", 16))
    label_source.pack(pady=20)
    label_destination = tk.Label(root, text=f"Destination folder: {destination_path}", font=("Arial", 16))
    label_destination.pack(pady=20)

    output_root = os.path.join(destination_path, 'compressed')
    
    label_message = tk.Label(root, text=f"Compressing...", font=("Arial", 22))
    label_message.pack(pady=20)

    def compression_task():
        find_video(folder_path, output_root)
        label_message.config(text=f"Compression finished.")
    
    compression_thread = threading.Thread(target=compression_task)
    compression_thread.start()    

if __name__ == "__main__":
    main()
