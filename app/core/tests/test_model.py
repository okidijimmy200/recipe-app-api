from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='test@test.com', password='test123'):
    '''create a sample user'''
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    # create a new test class
    def test_create_user_with_email_successful(self):
        '''test creating a new user with an email successful'''
        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        # run assertion to make sure user was created correctly
        self.assertEqual(user.email, email) #make sure email is the same
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''test the email for new user is normalized'''
        email = 'test@TEST.com'
        user = get_user_model().objects.create_user(email, 'test123') #password test123

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        # incase we pass a blank string in email
        with self.assertRaises(ValueError):
            # this shd raise a valueError else the test fails
            get_user_model().objects.create_user(None, 'test123')

    # test to check if the superuser is created and is assigned is_staff and is_superuser
    def test_create_new_superuser(self):
        '''test creating a new superuser'''
        user = get_user_model().objects.create_superuser(
            'test@admin.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

# model to create a tag
    def test_tag_str(self):
        '''test the tag string representation'''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

# testing ingredients
    def test_ingredient_str(self):
        '''test the ingredient string representation'''
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)


    
    def test_recipe_string(self):
        # test to convert our recipe to string
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='steak and mushroom sauce',
            time_minutes=5,
            price=5.80 
        )
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        '''test that image is saved in the correct location'''
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        # call function to call file path
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'upload/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
