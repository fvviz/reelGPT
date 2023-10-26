from pytube import YouTube
import uuid
import os

class ExtractVideo:
    def __init__(self):
        self.VID_ID= str(uuid.uuid4())
        self.FOLDER = "./experimental"
        self.FILE_NAME = os.path.join(self.FOLDER, f"{self.VID_ID}.mp4")
    def extract(self, link):
        yt = YouTube(link)
        vid = yt.streams.filter(file_extension='mp4').first()
        vid.download(filename=self.FILE_NAME)
        return self.FILE_NAME


