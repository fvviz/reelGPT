import argparse
from utils.transcription import ExtractVideo, TranscriptionModel
from utils.content_production import timestamp_to_seconds, clip_video
from utils.llm_process import ReelSelection
from utils.subtitle_overlay import SubtitleOverlay
import os

def start(LINK, MODEL):

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

    sub_overlay = SubtitleOverlay(vid_path, srt_out) 
    sub_overlay.overlay_subtitle()
    print("Overlayed subtitles")

    st = timestamp_to_seconds(out['start_time'])
    et = timestamp_to_seconds(out['end_time'])

    print("Extracted timestamps")

    clip_video(st, et, "final_output.mp4", "out/final_output.mp4")

    print("Clipped Video")


