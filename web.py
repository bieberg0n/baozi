import baozi
from flask import Flask, send_file, request
from gevent.wsgi import WSGIServer


app = Flask(__name__)
bz = baozi.Baozi()
# log(check_song(song, parser, yun))


@app.route('/query', methods=['POST'])
def query():
    song_str = request.json.get('song')
    pz, err = bz.check_song(song_str)
    r = '\n'.join(pz) + '\n\n' + '\n'.join(err)
    return r


@app.route('/', methods=['GET'])
def index():
    return send_file('static/index.html')


# app.run(debug=True)
WSGIServer(('', 8082), app).serve_forever()
