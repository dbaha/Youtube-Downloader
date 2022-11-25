import os
import subprocess
import pytube 
from moviepy.editor import *

def mp4_to_mp3(mp4, mp3):    
     mp4_without_frames = AudioFileClip(mp4)     
     mp4_without_frames.write_audiofile(mp3)     
     mp4_without_frames.close() 

yt = pytube.YouTube('https://www.youtube.com/watch?v=85nSayZ24Bo')
mp4_files=yt.streams.get_audio_only("mp4")  
vids= yt.streams.all()
# for i in range(len(vids)):
#     print(i,'. ',vids[i])
# vnum = int(input("Enter vid num: "))
parent_dir = r"C:\Work"
# vids[vnum].download(parent_dir)
mp4_files.download(parent_dir)
# userinput = input("default name?(y/n): ")
default_filename = mp4_files.default_filename
new_filename = default_filename.replace('mp4','mp3')

mp4_path=parent_dir+"\\"+default_filename
mp3_path=parent_dir+"\\"+new_filename
mp4_to_mp3(mp4_path,mp3_path)
os.remove(mp4_path)
print('done')

