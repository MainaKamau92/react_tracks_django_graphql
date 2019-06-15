import json
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from .test_fixture import login_user_query

User = get_user_model()


class BaseConfiguration(TestCase):
    @classmethod
    def setUpClass(cls):
        # We need to first run setUpClass function that we
        # inherited from TestCase.
        super(BaseConfiguration, cls).setUpClass()

        # Set up test client for all test classes
        # that will inherit from this class.
        cls.client = Client()

    @classmethod
    def query(cls, query: str = None):
        # Method to run all queries and mutations for tests.
        body = dict()
        body['query'] = query
        response = cls.client.post(
            '/tracks/', json.dumps(body), content_type='application/json')
        json_response = json.loads(response.content.decode())
        return json_response

    @classmethod
    def query_with_token(cls, access_token, query: str = None):
        # Method to run queries and mutations using a logged in user
        # with an authentication token
        body = dict()
        body['query'] = query
        http_auth = 'JWT {}'.format(access_token)
        url = '/tracks/'
        content_type = 'application/json'

        response = cls.client.post(
            url,
            json.dumps(body),
            HTTP_AUTHORIZATION=http_auth,
            content_type=content_type)

        json_response = json.loads(response.content.decode())
        return json_response

    def user_login(self):
        """
        Log in registered user and return a token
        """
        response = self.query(login_user_query.format(**self.login_user))
        return response['data']['tokenAuth']['token']

    def user2_login(self):
        """
        Log in registered user and return a token
        """
        response = self.query(login_user_query.format(**self.login_user2))
        return response['data']['tokenAuth']['token']

    def register_user(self, user):
        """
        register a new user
        """
        email = user["email"]
        username = user["username"]
        password = user["password"]
        user = User.objects.create_user(
            email=email, username=username, password=password)
        user.is_active = True
        user.save()
        return user

    def setUp(self):
        """
        Configurations to be made available before each
        individual test case inheriting from this class.
        """
        self.new_user = {
            "email": "johndoe@test.com",
            "username": "johndoe",
            "password": "johndoe123"
        }
        self.new_user2 = {
            "email": "philipdoe@test.com",
            "username": "philipdoe",
            "password": "philipdoe123"
        }

        self.login_user = {
            "username": "johndoe",
            "password": "johndoe123"
        }
        self.login_user2 = {
            "username": "philipdoe",
            "password": "philipdoe123"
        }
        self.user = self.register_user(self.new_user)
        self.user2 = self.register_user(self.new_user2)
        self.access_token = self.user_login()
        self.access_token2 = self.user2_login()
