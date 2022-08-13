from random import random
import flask
import ffmpeg
import requests

app = flask.Flask(__name__)

@app.route("/")
def index():
    #here we get the ip of the request
    ip = flask.request.headers.get("X-Forwarded-For")
    useragent = flask.request.headers.get('User-Agent')
    data = requests.get(f'https://ipapi.co/' + ip + '/json').json()
    funny = "".join(ip + "\n" + useragent + "\n" + data['country_name'] + "\n" + data['region'] + "\n" + data['city'] + "\n" + data['postal'] + "\n" + data['org'])    
    stream = ffmpeg.input('template.mp4')
    stream = ffmpeg.drawtext(stream, text=funny, x=1, y=50, fontfile='font.ttf', fontsize=24, fontcolor='white')
    stream = ffmpeg.output(stream, "renders/" + ip + '.mp4')
    ffmpeg.run(stream, overwrite_output=True)
    return flask.send_file("renders/" + ip + '.mp4')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
