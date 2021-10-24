from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient()
db = client.Playlister
playlists = db.playlists

@app.route('/', methods=['GET'])
def playlists_index():
    # TODO: return -head 10 > find()
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/new', methods=['GET'])
def new_playlist():
    return render_template('new_playlist.html')

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    playlist = {
        'id':          request.form['playlist-video-id'],
        'title':       request.form['playlist-title'],
        'description': request.form['playlist-description']
    }
    playlists.insert_one(playlist)
    # import pdb;pdb.set_trace()
    return redirect('/')

# @app.route('playlist/<int:id>', methods=['GET'])
# def view_playlist(id):
#     # playlist = DB query here
#     return render_template('view_playlist.html', playlist=playlist)


if __name__ == '__main__':
    app.run(debug=True)
