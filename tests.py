from unittest import TestCase, main as unittest_main, mock
from app import app, video_url_creator
from bson.objectid import ObjectId

sample_id_list     = ['SsKT0s5J8ko', 'RB-RcX5DS5A']
sample_playlist_id = ObjectId('5d55cffc4a3d4031f42827a3')

sample_playlist = {
    'title': 'Diablo',
    'description': 'Night Playlist',
    'videos': ['https://youtube.com/embed/SsKT0s5J8ko',
               'https://youtube.com/embed/RB-RcX5DS5A'
               ],
    'video_ids': ['SsKT0s5J8ko', 'RB-RcX5DS5A']
}

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
                         'https://youtube.com/embed/RB-RcX5DS5A'
                         ]

        self.assertEqual(output_list, expected_list)

    def test_index(self):
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('Playlist', page_content)

    def test_new_page(self):
        result = self.client.get('/playlists/new')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('New Playlist', page_content)

    def test_edit_page(self):
        result = self.client.get(f'/playlists/{sample_playlist_id}/edit')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('Edit Playlist', page_content)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_playlist(self, mock_find):
        mock_find.return_value = sample_playlist

        result = self.client.get(f'/playlists/{sample_playlist_id}')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('Diablo', page_content)

    # # Does not pass an _id when creating an item in DB
    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_playlist(self, mock_insert):
        result = self.client.post('/playlists', data=sample_form_data)

        mock_insert.assert_called_with(sample_playlist)
        self.assertEqual(result.status, '302 FOUND')

    # @mock.patch('pymongo.collection.Collection.update_one')
    # def test_update_playlist(self, mock_update):
    #     result = self.client.post(f'/playlists/{sample_playlist_id}', data=sample_form_data)
    #
    #     self.assertEqual(result.status, '302 FOUND')
    #     mock_update.assert_called_with({'_id': sample_playlist_id}, {'$set': sample_playlist})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_playlist(self, mock_delete):
        form_data = {'_method': 'POST'}
        result = self.client.post(f'/playlists/{sample_playlist_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        # mock_delete.assert_called_with({'_id': sample_playlist_id})


if __name__ == '__main__':
    unittest_main()
