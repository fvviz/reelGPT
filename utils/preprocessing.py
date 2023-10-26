
import os
from pydub import AudioSegment
from extract_vid import ExtractVideo

class AudioPreprocessor:
    def __init__(self, FILE_PATH) -> None:
        # Defining imp constants
        self.FILE_PATH= FILE_PATH
        self.initial_file_name = os.path.basename(self.FILE_PATH)
        self.DIR = os.path.dirname(FILE_PATH)

        # Start by converting the given video into an audio segment object.
        # Audio segment is saved as mp3


        self.audio_seg = AudioSegment.from_file(self.FILE_PATH, self.initial_file_name.split(".")[-1])
        self.audio_seg_file_name = self.initial_file_name.replace(".mp4","_audio_seg.mp3")
        self.audio_seg_path = os.path.join(self.DIR, self.audio_seg_file_name)
        self.audio_seg.export(self.audio_seg_path)

        # Chunk count defines how many chunks we will be splitting the input video into

        self.chunk_count = 1
        self.file_size = self.get_file_size(self.audio_seg_path)

        # Ff the saved audio segment is greater than 25mb, 
        # Continously half*duration of the audio seg until a file smaller than 25 mb obtained
        # Each iteration will double chunk count

        while self.file_size>25:
            print(self.chunk_divisor, ":filesize greater than 25")
            self.chunk_count*=2
            self.audio_seg_file_name, self.audio_seg = self.get_halfed_file()
            self.file_size = self.get_file_size(os.path.join(self.DIR, self.audio_seg_file_name))
        
    def get_file_size(self, path_to_file):
        file_size_byes= os.stat(path_to_file).st_size
        return file_size_byes/(1024*1024)
    
    def get_halfed_file(self):
        half_dur = len(self.audio_seg)/2
        halfed_audio_seg = self.audio_seg[:half_dur]
        halfed_audio_seg_filename = self.audio_seg_file_name.replace('.mp3', f'_split_{self.chunk_divisor}.mp3')
        halfed_audio_seg.export(os.path.join(self.DIR, halfed_audio_seg_filename))
        return halfed_audio_seg_filename, halfed_audio_seg

