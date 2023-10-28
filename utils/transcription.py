from pytube import YouTube
from pathlib import Path
from whisper.utils import get_writer
import whisper
import torch
import os
from pytube import YouTube
import uuid
import os



class ExtractVideo:
    def __init__(self, directory):
        self.VID_ID= str(uuid.uuid4())
        self.FOLDER = directory
        self.FILE_NAME = os.path.join(self.FOLDER, f"{self.VID_ID}.mp4")


    def extract_youtube_audio(self, url):
        yt = YouTube(url)
        yt = (yt.streams
                .filter(only_audio = True, file_extension = "mp4")
                .order_by("abr")
                .desc())
        return yt.first().download(filename = self.FILE_NAME)
    
    def extract_video(self, url):
        yt = YouTube(url)
        vid = yt.streams.filter(file_extension='mp4').first()
        save_path = os.path.join(self.FOLDER, f"{self.VID_ID}_full_vid.mp4")
        vid.download(filename=save_path)
        return save_path




class TranscriptionModel:
    def __init__(self,filepath, MODEL='small', language='hi'):
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        self.file = Path(filepath)
        self.language= language
        
        self.model = whisper.load_model(MODEL).to(DEVICE)

    def transcribe_file(self, srt=True, plain=False):
        print(f"Transcribing file: {self.file}\n")

        output_directory = self.file.parent
        options = {
        'max_line_width': None,
        'max_line_count': None,
        'highlight_words': False
        }

        result = self.model.transcribe(self.file, verbose = False, language=self.language)

        if plain:
            txt_path = self.file.with_suffix(".txt")
            print(f"\nCreating text file")

            with open(txt_path, "w", encoding="utf-8") as txt:
                txt.write(result["text"])
        if srt:
            print(f"\nCreating SRT file")
            srt_writer = get_writer("srt", output_directory)
            srt_writer(result, str(self.file.stem), options)
            srt_path = os.path.join(self.file.stem, ".srt")
            print("Srt filed saved to:", srt_path)

        return srt_path










