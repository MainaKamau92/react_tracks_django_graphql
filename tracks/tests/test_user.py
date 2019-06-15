from .BaseConfig import BaseConfiguration
from .test_fixture import users_query, user_query, user_ghost_query, create_user
from graphql import GraphQLError


class UserTestCase(BaseConfiguration):

    def test_users_query(self):
        response = self.query(users_query)
        data = response.get('data')
        self.assertEquals(data.get('users'), [{'id': '1', 'username': 'johndoe'}, {
                          'id': '2', 'username': 'philipdoe'}])

    def test_user_query(self):
        response = self.query(user_query)
        data = response.get('data')
        self.assertEquals(data.get('user'), {'id': '1', 'username': 'johndoe'})

    def test_ghost_user_query(self):
        self.query(user_ghost_query)
        self.assertRaises(GraphQLError)

    def test_create_user(self):
        response = self.query(create_user)
        data = response.get('data')
        self.assertEquals(data, {"createUser": {
            "user": {
                "id": "3",
                "email": "jackdoe@test.com"
            }}
        })
