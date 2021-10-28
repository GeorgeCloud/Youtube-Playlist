from unittest import TestCase, main as unittest_main, mock
from app import app, video_url_creator
from bson.objectid import ObjectId

sample_id_list     = ['SsKT0s5J8ko', 'WhlKJH3KTBU']
sample_playlist_id = ObjectId('5d55cffc4a3d4031f42827a3')

sample_playlist = {
    'title': 'Diablo',
    'description': 'Night Playlist',
    'videos': ['https://youtube.com/embed/SsKT0s5J8ko',
               'https://youtube.com/embed/WhlKJH3KTBU'
               ],
    'video_ids': ['SsKT0s5J8ko', 'WhlKJH3KTBU']
}

# sample_form_data = {
#     'title': sample_playlist['title'],
#     'description': sample_playlist['description'],
#     'videos_ids': ' '.join(sample_playlist['video_ids'])
# }

sample_form_data = {
    'title': sample_playlist['title'],
    'description': sample_playlist['description'],
    'video_ids': ' '.join(sample_playlist['video_ids'])
}


class PlaylistsTests(TestCase):
    def setUp(self):
        self.client = app.test_client()

        app.config['TESTING'] = True

    def test_video_url_creator(self):
        output_list = video_url_creator(sample_id_list)
        expected_list = ['https://youtube.com/embed/SsKT0s5J8ko',
                         'https://youtube.com/embed/WhlKJH3KTBU'
                         ]

        self.assertEqual(output_list, expected_list)

    def test_index(self):
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('Playlist', page_content)

    def test_new(self):
        result = self.client.get('/playlists/new')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('New Playlist', page_content)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_playlist(self, mock_find):
        mock_find.return_value = sample_playlist

        result = self.client.get(f'/playlists/{sample_playlist_id}')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('Diablo', page_content)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_playlist(self, mock_insert):
        result = self.client.post('/playlists', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        # mock_insert.assert_called_with(sample_playlist)

    def test_edit(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass


if __name__ == '__main__':
    unittest_main()