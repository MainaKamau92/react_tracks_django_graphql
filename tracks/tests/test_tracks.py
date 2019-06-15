from .BaseConfig import BaseConfiguration
from .test_fixture import (test_tracks_query, create_track, update_track,
                           delete_track, filter_query, create_like, query_likes, create_like_ghost_track)
from graphql import GraphQLError


class TracksTestCase(BaseConfiguration):

    def test_tracks_query(self):
        response = self.query(test_tracks_query)
        data = response.get('data')
        print(response)
        self.assertEquals(data.get('tracks'), [])

    def test_create_track(self):
        response = self.query_with_token(self.access_token, create_track)
        data = response.get('data')
        self.assertEquals(
            data, {'createTrack': {'track': {'id': '1', 'description': 'I am not afraid'}}})

    def test_update_track(self):
        self.test_create_track()
        response = self.query_with_token(self.access_token, update_track)
        data = response.get('data')
        self.assertEquals(
            data, {'updateTrack': {'track': {'id': '1', 'description': 'I am afraid'}}})

    def test_delete_track(self):
        self.test_create_track()
        response = self.query_with_token(self.access_token, delete_track)
        data = response.get('data')
        self.assertEquals(data, {'deleteTrack': {'trackId': 1}})

    def test_query_filter(self):
        self.test_create_track()
        response = self.query_with_token(self.access_token, filter_query)
        data = response.get('data')
        self.assertEquals(
            data, {'tracks': [{'id': '1', 'title': 'Not Afraid', 'likes': []}]})

    def test_create_likes(self):
        self.test_create_track()
        response = self.query_with_token(self.access_token, create_like)
        data = response.get('data')
        self.assertEquals(
            data, {'createLike': {'track': {'description': 'I am not afraid',
                                            'id': '1',
                                            'title': 'Not Afraid',
                                            'url': 'http://notafraid.com'},
                                  'user': {'email': 'johndoe@test.com',
                                           'id': '1',
                                           'username': 'johndoe'}}})

    def test_query_likes(self):
        self.test_create_likes()
        response = self.query_with_token(self.access_token, query_likes)
        data = response.get('data')
        self.assertEquals(data, {"likes": [
            {
                "id": "1",
                "user": {
                    "username": "johndoe"
                },
                "track": {
                    "title": "Not Afraid"
                }
            }
        ]
        })

    def test_unauthorized_user_cant_create_track(self):
        self.query(create_track)
        self.assertRaises(GraphQLError)

    def test_only_owner_can_update_track(self):
        self.test_create_track()
        self.query(update_track)
        self.assertRaises(GraphQLError)

    def test_only_logged_in_user_can_delete_track(self):
        self.test_create_track()
        self.query(delete_track)
        self.assertRaises(GraphQLError)

    def test_only_owner_can_delete_track(self):
        self.test_create_track()
        self.query_with_token(self.access_token2, delete_track)
        self.assertRaises(GraphQLError)

    def test_only_logged_in_users_like_tracks(self):
        self.test_create_track()
        self.query(create_like)
        self.assertRaises(GraphQLError)

    def test_cant_like_inexistent_track(self):
        self.query_with_token(self.access_token, create_like_ghost_track)
        self.assertRaises(GraphQLError)


