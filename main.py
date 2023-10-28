from utils.transcription import ExtractVideo, TranscriptionModel
from utils.content_production import timestamp_to_seconds, clip_video
from utils.LLM_process import ReelSelection
import os


LINK = "https://www.youtube.com/watch?v=sN73s23qVXw&ab_channel=RahulGandhi"
MODEL = "small"



ev=  ExtractVideo(directory=".")
audio = ev.extract_youtube_audio(LINK)

transcription_model = TranscriptionModel(audio, MODEL)
srt_out = transcription_model.transcribe_file()
rs = ReelSelection(srt_out)
out = rs.get_imp_parts()

vid_path = ev.extract_video(LINK)

st = timestamp_to_seconds(out['start_time'])
et = timestamp_to_seconds(out['end_time'])



clip_video(st, et, vid_path, os.path.join(os.path.dirname(vid_path), "final_output.mp4"))
