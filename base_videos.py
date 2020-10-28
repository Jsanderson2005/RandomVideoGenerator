from __future__ import unicode_literals
import youtube_dl
import os

ydl_opts = {
    'outtmpl': os.path.join('./videos', '%(title)s.%(ext)s'),
}

urlList = ["https://www.youtube.com/watch?v=qi2oaQjSKQk",
    "https://www.youtube.com/watch?v=vyl5Mwr84MA",
    "https://www.youtube.com/watch?v=1GgONMugB14",
    "https://www.youtube.com/watch?v=o48KzPa42_o",
    "https://www.youtube.com/watch?v=LSj37NGafko",
    "https://www.youtube.com/watch?v=QFxjM-6AStA",
    "https://www.youtube.com/watch?v=rz5TGN7eUcM",
    "https://www.youtube.com/watch?v=VCvC4_6zkrs",
    "https://www.youtube.com/watch?v=lYz1Cj0Nfds",
    "https://www.youtube.com/watch?v=OJcRgn1UgoM",
    "https://www.youtube.com/watch?v=XyTsjlqoyBY",
    "https://www.youtube.com/watch?v=EF0J7Bt9spQ",
    "https://www.youtube.com/watch?v=JUfO9YRUKes",
    "https://www.youtube.com/watch?v=2WAle7UceU4",
    "https://www.youtube.com/watch?v=ZapOy3eH3yE",
    "https://www.youtube.com/watch?v=96wgjKfFtpY"]

for i in urlList:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([i])