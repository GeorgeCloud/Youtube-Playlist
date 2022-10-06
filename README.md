# Youtube-Playlist
Youtube Playlist allows you to create a playlist with youtube ids.

Live on --> https://playlister-gc.herokuapp.com/

Steps to run

1. clone project
```bash
git clone https://github.com/GeorgeCloud/Youtube-Playlist.git
```

2. Run Project either local or through docker
    - Local
      ```bash
        pip3 install requirements.txt
      ```
      - Add custom external database (OPTIONAL)
        ```bash
          echo > "MONGODB_URI=<your_connection_string>" > .env
        ```
       Now start project:
       ```bash
        python app.py
      ```
     - Docker
        ```bash
          echo "MONGODB_URI='mongodb://mongo:27017/YoutubePlaylist'" > .env
        ```
        ```bash
          docker compose build
        ```
        ```bash
          docker compose up
        ```
    
  3. Open Running Project
    http://localhost:8000/
    
