from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# test client to make request to API
from rest_framework.test import APIClient
from rest_framework import status

TOKEN_USER_URL = reverse('user:token') #reverse to generate token
CREATE_USER_URL = reverse('user:create') #reverse user:create url variable
ME_URL = reverse('user:me')

# helper function to perform generic tasks
def create_user(**params):
    return get_user_model().objects.create_user(**params)
    

# public user api test(public, not authenticated)
class PublicUserApiTests(TestCase):
    '''Test the user api public'''
    def setUp(self):
        self.client = APIClient()

    # test to validate the user is created correctly
    def test_create_valid_user_successful(self):
        # sample payload
        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        # expect http 200 OK
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data) # take the dic res and pass it as response
        self.assertTrue(user.check_password(payload['password']))
        # to  make sure password is not returned in req
        self.assertNotIn('password', res.data)

    # test to check if the user is created but the user already exists
    def test_user_exists(self):
        payload = {'email': 'test@test.com', 'password': 'test123'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''test tht the password must be more thn 5 characters'''
        payload = {'email': 'test@test.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''test tht a token is created for a user'''
        payload = {'email': 'test@test.com', 'password': 'password123'}
        create_user(**payload)
        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertIn('token', res.data) #check whether there is a key in token sent
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        '''token is not created if invalid credentials are given'''
        create_user(email='test@test.com', password='test123')
        payload = {'email': 'test@test.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        '''test tht token is not created if user doesnot exit'''
        payload = {'email': 'test@test.com', 'password': 'password123'}
        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        '''test tht email and password are required'''
        res = self.client.post(TOKEN_USER_URL, {'email': 'one', 'password': ''})
        self.assertNotEqual('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        '''test tht authentication is required for users'''
        res = self.client.get(ME_URL)

        #if u call url without authentication, it returns 401
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# test for retrieve profile successful
class PrivateUserApiTest(TestCase):
    '''test API request tht requires authentication'''

    def setUp(self):
        self.user = create_user(
            email='test@test.com',
            password='test123',
            name='name'
        )
        # setup our client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user) #force_authenticate is used to make it easy to perform authentication test

    def test_retrieve_profile_success(self):
        '''test retrieving profile for logged in user'''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        '''test tht post is not allowed on the me url'''
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        '''test updating the user profile for authentication'''
        payload = {'name': 'new name', 'password': 'newpassword'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db() #geting latest value from db
        # verify each value from db is updated
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)