from __future__ import unicode_literals
import youtube_dl
import os
import json

with open('videoIDlist.json') as json_file:
        urlList = json.load(json_file)

ydl_opts = {
    'outtmpl': os.path.join('./videos', '%(title)s.%(ext)s'),
}
 

for i in urlList:
    i = "https://www.youtube.com/watch?v=" + i
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([i])