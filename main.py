import argparse
from utils.transcription import ExtractVideo, TranscriptionModel
from utils.content_production import timestamp_to_seconds, clip_video
from utils.llm_process import ReelSelection
from utils.subtitle_overlay import SubtitleOverlay
import os

parser = argparse.ArgumentParser(description="Process a YouTube link and generate a transcribed video clip.")

parser.add_argument("LINK", help="YouTube video link")
parser.add_argument("--model", help="Transcription model (default is 'tiny')", default="tiny")

args = parser.parse_args()


LINK = args.LINK
MODEL = args.model

print(f"Extracting link: {LINK} using model: {MODEL}")

ev = ExtractVideo(directory=".")
audio = ev.extract_youtube_audio(LINK)

print(f"Extracted video and audio")

transcription_model = TranscriptionModel(audio, MODEL)
srt_out = transcription_model.transcribe_file()
rs = ReelSelection(srt_out)
out = rs.get_imp_parts()

print(f"Extracted transcription and important parts")

vid_path = ev.extract_video(LINK)

st = timestamp_to_seconds(out['start_time'])
et = timestamp_to_seconds(out['end_time'])

print("Extracted timestamps")

clip_video(st, et, vid_path, os.path.join(os.path.dirname(vid_path), "final_output.mp4"))

print("Clipped Video")

sub_overlay = SubtitleOverlay(os.path.join(os.path.dirname(vid_path), "final_output.mp4"), srt_out, out['start_time'], out['end_time'])
sub_overlay.fix_subtitle()
sub_overlay.overlay_subtitle()

print("Overlayed subtitles")