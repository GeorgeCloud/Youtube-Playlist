from flask import Flask, render_template, request, url_for, redirect
from flask_paginate import Pagination, get_page_parameter
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
client = MongoClient()
db = client.Playlister
playlists = db.playlists

PLAYLISTS_PER_PAGE = 1

def video_url_creator(id_lst):
    return [f'https://youtube.com/embed/{id}' for id in id_lst]

def create_playlist_document(request_data):
    video_ids = request.form['video_ids'].split()
    return {
        'title': request.form['title'],
        'description': request.form['description'],
        'rating': int(request.form['rating']),
        'videos': video_url_creator(video_ids),
        'video_ids': video_ids,
        'views': 1,
        'last_modified': datetime.now(),
    }

@app.route('/', methods=['GET'])
def playlists_index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=playlists.count_documents({}), search=False, record_name='playlists')

    return render_template('playlists_index.html', playlists=playlists.find(), pagination=pagination)  # paginate

@app.route('/playlists/new', methods=['GET'])
def playlist_new():
    return render_template('new_playlist.html', playlist='', title="New Playlist")

@app.route('/playlists', methods=['POST'])
def playlist_submit():
    playlist_document = create_playlist_document(request.form)

    playlist_id = playlists.insert_one(playlist_document).inserted_id
    return redirect(url_for('playlist_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>', methods=['GET'])
def playlist_show(playlist_id):
    playlist = playlists.find_one_and_update(
        {'_id': ObjectId(playlist_id)},
        {'$inc': {'views': 1}}
    )
    return render_template('playlists_show.html', playlist=playlist)

@app.route('/playlists/<playlist_id>/edit', methods=['GET'])
def playlist_edit(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title="Edit Playlist")

@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlist_update(playlist_id):
    playlist_document = create_playlist_document(request.form)

    playlists.find_one_and_update(
        {'_id': ObjectId(playlist_id)},
        {'$set': playlist_document}
    )

    return redirect(url_for('playlist_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>/delete')
def playlist_delete(playlist_id):
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


if __name__ == '__main__':
    app.run(debug=True)
