from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


app = Flask(__name__)
client = MongoClient()
db = client.Playlister
playlists = db.playlists

def video_url_creator(id_lst):
    return [f'https://youtube.com/embed/{id}' for id in id_lst]

@app.route('/', methods=['GET'])
def playlists_index():
    # TODO: return -head 10 > find()
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)

@app.route('/playlists/new', methods=['GET'])
def new_playlist():
    return render_template('new_playlist.html')

@app.route('/playlists', methods=['POST'])
def submit_playlist():
    video_ids = request.form['video_ids'].split()
    playlist = {
        'title':       request.form['title'],
        'description': request.form['description'],
        'videos':      video_url_creator(video_ids),
        'video_ids':   video_ids
    }
    playlists.insert_one(playlist)
    # import pdb;pdb.set_trace()
    return redirect(url_for('playlists_show', playlist_id=str(playlist["_id"])))

@app.route('/playlists/edit/<playlist_id>')
def edit_playlist(playlist_id):
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))

@app.route('/playlists/delete/<playlist_id>')
def delete_playlist(playlist_id):
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


if __name__ == '__main__':
    app.run(debug=True)
