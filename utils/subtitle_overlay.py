import pysrt
from datetime import datetime
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

class SubtitleOverlay():
    def __init__(self, video_path, subtitle_file_path):
        self.video_path = video_path
        self.subtitle_file_path = subtitle_file_path
    

    def overlay_subtitle(self):
        
        def time_to_seconds(time_obj):
            return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000


        def create_subtitle_clips(subtitles, videosize,fontsize=32, font='Nirmala-UI-Bold', color='white', debug = False):
            subtitle_clips = []

            for subtitle in subtitles:
                start_time = time_to_seconds(subtitle.start)
                end_time = time_to_seconds(subtitle.end)
                duration = end_time - start_time

                video_width, video_height = videosize
                
                text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color, bg_color = 'black',size=(video_width*3/4, None), method='caption').set_start(start_time).set_duration(duration)
                subtitle_x_position = 'center'
                subtitle_y_position = video_height* 4 / 5 

                text_position = (subtitle_x_position, subtitle_y_position)                    
                subtitle_clips.append(text_clip.set_position(text_position))

            return subtitle_clips


        srtfilename = self.subtitle_file_path
        mp4filename = self.video_path
        video = VideoFileClip(mp4filename)
        subtitles = pysrt.open(srtfilename)
        print("length of subs : " + str(len(subtitles)))
        print("saved path" + self.subtitle_file_path)
        begin,end= mp4filename.split(".mp4")
        output_video_file = "final_output.mp4"

        print ("Output file name: ",output_video_file)

        subtitle_clips = create_subtitle_clips(subtitles,video.size)

        final_video = CompositeVideoClip([video] + subtitle_clips)

        final_video.write_videofile(output_video_file, threads = 8, fps=24)


"""
sup = SubtitleOverlay('rahul_gandhi_clipped.mp4', './RG.srt', '00:15:25,660', '00:16:21,140')
sup.fix_subtitle()
sup.overlay_subtitle()
"""
