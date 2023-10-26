from pydub import AudioSegment
import os

song = AudioSegment.from_file("./experimental/df56df70-a45b-42f6-9358-8c7d39dfa891.mp4", "mp4")

# PyDub handles time in milliseconds
half_dur = len(song)/(2000)
print(half_dur)

halfed = song[:half_dur]
print(halfed)

halfed.export("halfed.mp3", format='mp3')
#first_10_minutes = song[:ten_minutes]  

print(os.stat("halfed.mp3").st_size/(1024*1024))

#first_10_minutes.export("good_morning_10.mp3", format="mp3")