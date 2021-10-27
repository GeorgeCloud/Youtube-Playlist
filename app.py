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

def create_playlist_document(request_data):
    video_ids = request.form['video_ids'].split()
    return {
        'title': request.form['title'],
        'description': request.form['description'],
        'videos': video_url_creator(video_ids),
        'video_ids': video_ids
    }

@app.route('/', methods=['GET'])
def playlists_index():
    # TODO: return -head 10 > find()
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/<playlist_id>', methods=['GET'])
def playlists_show(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)

@app.route('/playlists/new', methods=['GET'])
def new_playlist():
    return render_template('new_playlist.html', playlist='')

@app.route('/playlists', methods=['POST'])
def submit_playlist():
    playlist_document = create_playlist_document(request.form)

    playlists.insert_one(playlist_document)
    return redirect(url_for('playlists_show', playlist_id=str(playlist_document["_id"])))

@app.route('/playlists/edit/<playlist_id>', methods=['GET'])
def edit_playlist(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist)

@app.route('/playlists/<playlist_id>', methods=['POST'])
def update_playlist(playlist_id):
    playlist_document = create_playlist_document(request.form)

    playlists.find_one_and_update(
        {'_id': ObjectId(playlist_id)},
        {'$set': playlist_document}
    )

    return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/delete/<playlist_id>')
def delete_playlist(playlist_id):
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


if __name__ == '__main__':
    app.run(debug=True)
