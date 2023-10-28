'''
from pydub import AudioSegment
import os

audio = AudioSegment.from_mp3("./experimental/60012d3a-0a28-46dc-8f46-c3c26af6e439_audio_seg.mp3")
out_path = os.path.join("./experimental", "current_chunks")
os.makedirs(out_path, exist_ok=True)
chunk_count = 4
chunk_duration = len(audio) / chunk_count

print(chunk_duration)

for i in range(chunk_count):
    chunk = audio[i*chunk_duration:(i+1)*chunk_duration]
    chunk.export(os.path.join(out_path,f"chunk_{i}.mp3"))

'''

from preprocessing import AudioPreprocessor

vid = AudioPreprocessor(FILE_PATH="./experimental/ae2950c5-85e7-47f3-b7a4-0f933a7104e6.mp4")
vid.split_to_chunks()