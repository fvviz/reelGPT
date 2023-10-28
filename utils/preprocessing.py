
import os
from pydub import AudioSegment
import shutil

class AudioPreprocessor:
    def __init__(self, FILE_PATH) -> None:
        self.FILE_PATH= FILE_PATH
        self.initial_file_name = os.path.basename(self.FILE_PATH)
        self.DIR = os.path.dirname(FILE_PATH)

        print("1) Segmenting Audio..")

        self.audio_seg = AudioSegment.from_file(self.FILE_PATH, self.initial_file_name.split(".")[-1])
        self.audio_seg_file_name = self.initial_file_name.replace(".mp4","_audio_seg.mp3")
        self.audio_seg_path = os.path.join(self.DIR, self.audio_seg_file_name)
        self.audio_seg.export(self.audio_seg_path)

        print("2) Audio file exported.")
        
        self.chunk_count = 1
        self.file_size = self.get_file_size(self.audio_seg_path)

        while self.file_size>25:
            print(f"File Larger than 25MB found, Splitting... |  CHUNK={self.chunk_count+1}")
            self.chunk_count*=2
            self.audio_seg_file_name, self.audio_seg = self.get_halfed_file()
            self.file_size = self.get_file_size(os.path.join(self.DIR, self.audio_seg_file_name))
        
        print(f"Initalised audio with {self.file_size}| CHUNKS= {self.chunk_count}")
    def get_file_size(self, path_to_file):
        file_size_byes= os.stat(path_to_file).st_size
        return file_size_byes/(1024*1024)
    
    def get_halfed_file(self):
        half_dur = len(self.audio_seg)/2
        halfed_audio_seg = self.audio_seg[:half_dur]
        halfed_audio_seg_filename = self.audio_seg_file_name.replace('.mp3', f'_split_{self.chunk_count}.mp3')
        halfed_audio_seg.export(os.path.join(self.DIR, halfed_audio_seg_filename))
        return halfed_audio_seg_filename, halfed_audio_seg
    
    def split_to_chunks(self):
        original_audio_seg = AudioSegment.from_mp3(self.audio_seg_path)
        current_chunks_dir = os.path.join(self.DIR, "current_chunks")

        if os.path.exists(current_chunks_dir):
            shutil.rmtree(current_chunks_dir)

        os.makedirs(current_chunks_dir, exist_ok=True) 

        if self.chunk_count>1:
            print(f"Exporting {self.chunk_count} chunks..")

            chunk_duration = len(original_audio_seg) / self.chunk_count
            for i in range(self.chunk_count):
                start_time = i * chunk_duration
                end_time = (i + 1) * chunk_duration

                chunk = original_audio_seg[start_time:end_time]
                chunk_filename = f"chunk_{i}.mp3"

                chunk_path = os.path.join(current_chunks_dir, chunk_filename)
                chunk.export(chunk_path, format="mp3")
        else:
            shutil.move(self.audio_seg_path, os.path.join(current_chunks_dir, "chunk_0.mp3"))

        
        
