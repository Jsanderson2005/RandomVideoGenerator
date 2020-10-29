import os
from flask import Flask, redirect, render_template, request, abort, send_file
from urllib.parse import urlparse, parse_qs
import random
import json
import youtube_dl
import glob

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

@app.route('/upload/api', methods=['GET'])
def upload_file():
    link = request.args.get('link')
    if link:
        result = video_id(link)
        if result == None:
            abort(400, 'Not a youtube link!')
        else:
            append_json(result)
            ydl_opts = {'outtmpl': os.path.join('./videos', '%(title)s.%(ext)s'),}
            youtube_link = "https://www.youtube.com/watch?v=" + result
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtube_link])
            except:
                abort(500, 'There was an error downloading the link')
            append_json(result)
            return redirect("/upload", code=302)
    
@app.route('/video.mp4', methods=['GET'])
def embed():
    return send_file(random_video(),attachment_filename='video.mp4')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 