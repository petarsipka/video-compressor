import ffmpeg
import os
import sys

VIDEO_EXTENSIONS = ('.3g2', '.3gp', '.asf', '.asx', '.avi', '.flv', '.m2ts', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv')

OUTPUT_ROOT = os.path.abspath('compressed')

def find_video(folderpath):
    for root, _, files in os.walk(folderpath):
        for file in files:
            if file.lower().endswith(VIDEO_EXTENSIONS):
                compress_video(os.path.join(root,file))

def compress_video(filepath):
    relative_path = os.path.relpath(filepath, start=sys.argv[1])
    output_path = os.path.join(OUTPUT_ROOT, relative_path)

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
    folder_path = os.path.abspath(sys.argv[1])
    find_video(folder_path)

if __name__ == "__main__":
    main()
