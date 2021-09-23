# mock behavior of django get db
from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

# command thrown when the db is not available

class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        '''test waiting for when the db is available'''
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # mock behavior of a function
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1) #to check how many times func is called

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        '''test waiting for db'''
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # create side effect to function we r mocking
            gi.side_effect = [OperationalError] * 5 + [True] #5 times, it will raise operational error and the 6th time it returns
            self.assertEqual(gi.call_count, 0)
        
        
