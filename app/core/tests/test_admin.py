from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    # setup functions tht need to be run  b4 any other test
    def setUp(self):
        self.client = Client() #set to test client variable
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@admin.com',
            password = 'password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@admin.com',
            password = 'password123',
            name = 'Test user full name'
        )

    # create our test for listing user
    def test_users_listed(self):
        '''test tht the users r listed on user page'''
        url = reverse('admin:core_user_changelist') #we use reverse url
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email) #assertContains makes sure the res contains the required statuscodes and other contents

    # test tht the change page renders correctly
    def test_user_change_page(self):
        '''test tht the user edit page works'''
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # test the page renders OK
        self.assertEqual(res.status_code, 200)

    # add test for add page
    def test_create_user_page(self):
        '''test tht the create user page works'''
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
