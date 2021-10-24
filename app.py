from flask import Flask, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient()
db = client.Playlister

@app.route('/', methods=['GET'])
def index():
    # TODO: return -head 10 > find()
    return render_template('view_playlists.html', playlists=playlists.find())

# @app.route('playlist/<int:id>', methods=['GET'])
# def view_playlist(id):
#     # playlist = DB query here
#     return render_template('view_playlist.html', playlist=playlist)


if __name__ == '__main__':
    app.run(debug=True)
