from moviepy.editor import *
import os
def timestamp_to_seconds(timestamp):
    parts = timestamp.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2].replace(',', '.'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def clip_video(start_time, end_time, input_path, save_path):
        clip = VideoFileClip(input_path)
        clip = clip.subclip(start_time, end_time)
        clip.write_videofile(save_path, codec='libx264')
        
