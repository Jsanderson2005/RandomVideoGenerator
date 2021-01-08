import os
from flask import Flask, redirect, render_template, request, abort, send_file
from urllib.parse import urlparse, parse_qs
import random
import json
import youtube_dl
import glob
import smtplib
from email.message import EmailMessage
import urllib.request
import mimetypes
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

def get_file_name_type(path):
    firstpos=path.rfind("/")
    lastpos=len(path)
    return path[firstpos+1:lastpos]

def get_file_name(path):
    firstpos=path.rfind("/")
    lastpos=path.rfind(".")
    return path[firstpos+1:lastpos]

app = Flask(__name__)


def open_json():
    with open('videoIDlist.json') as json_file:
        data = json.load(json_file)
        return data


def append_json(data):
    with open('videoIDlist.json') as json_file:
        jsondata = json.load(json_file)
    jsondata.append(data)
    with open('videoIDlist.json', 'w') as outfile:
        json.dump(jsondata, outfile)


def random_video_link():
    json_data = open_json()
    return "https://www.youtube.com/embed/" + random.choice(json_data)


def video_id(value):
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

def random_video():
    video_list = glob.glob("./videos/*.mp4")
    return random.choice(video_list)

@app.route('/')
def index():
    return render_template('new_index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/upload/api', methods=['GET'])
def upload_link():
    link = request.args.get('link')
    if link:
        result = video_id(link)
        if result == None:
            path = link
            mimetypes.init()
            mimestart = mimetypes.guess_type(path)[0]
            if mimestart != None:
                mimestart = mimestart.split('/')[0]
                if mimestart == 'video':
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(path, './temp/' + get_file_name_type(path)) 
                    filePath =  './temp/' + get_file_name_type(path)
                    clip = VideoFileClip(filePath)
                    clip.write_videofile("./videos/" + get_file_name(path) + '.mp4')
                    os.remove(filePath) 
                    return redirect("/success", code=302)
                else:
                    abort(400, 'This is not a recognised link!')
            else:
                abort(400, 'This is not a recognised link!')
        else:
            append_json(result)
            ydl_opts = {'outtmpl': os.path.join('./videos', '%(title)s.%(ext)s'),}
            youtube_link = "https://www.youtube.com/watch?v=" + result
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtube_link])
            except:
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([youtube_link])
                except:
                    abort(500, 'There was an error downloading the youtubelink')
            append_json(result)
            return redirect("/success", code=302)

@app.route('/report/api', methods=['GET'])
def report_api():
    title = request.args.get('title')
    message = request.args.get('message')
    gmail_user = 'randomvideogeneratoronline@gmail.com'
    gmail_password = 'Ch4rlieTheD0g2019'
    sent_from = gmail_user
    to = "Joshua@thisisthesandersons.co.uk"
    subject = '[RANDOM VIDEO GENERATOR] ' + title 
    msg = EmailMessage()
    msg.set_content(message)
    msg['From'] = sent_from
    msg['To'] = to
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, msg.as_string())
        server.close()
        print("\n")
        print("SENT MESSAGE: \n" + msg.as_string())
        return redirect("/success", code=302)
    except:
        abort(500, 'There was an error submitting your request at this time, please try again later.')

    return redirect("/success", code=302)

@app.route('/report', methods=['GET'])
def report():
    return render_template('feedback.html')

@app.route('/video.mp4', methods=['GET'])
def embed():
    return send_file(random_video())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 