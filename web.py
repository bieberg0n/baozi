import sys
import baozi
from flask import Flask, send_file, request, jsonify
from gevent.wsgi import WSGIServer
# from utils import log


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
bz = baozi.Baozi()
# log(check_song(song, parser, yun))


def result(query: dict):
    song_str = query.get('song')
    try:
        result = bz.check_song(song_str)
    except IndexError as e:
        result = {
            'err': ['Check error'],
            'song_pz': [],
            'tail_yuns': []
        }
    return result


@app.route('/yun', methods=['POST'])
def yun():
    keyword = request.json.get('keyword')
    result = [bz.yun.yun_from_char(char) for char in keyword]
    return jsonify(result)


@app.route('/query', methods=['POST'])
def query():
    songs = request.json
    results = [result(song) for song in songs]
    # log(results)
    return jsonify(results)


@app.route('/', methods=['GET'])
def index():
    return send_file('static/index.html')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app.run(debug=True)
    else:
        WSGIServer(('', 8082), app).serve_forever()
