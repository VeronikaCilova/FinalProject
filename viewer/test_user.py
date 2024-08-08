from django.contrib.auth.models import User
from django.test import TestCase


class UserTestSelenium(TestCase):
    def setUp(self):
        user_one = User(username='magdalena', email='magdalena@firm.cz')
        # User.objects.create()
        user_one_pw = 'nereknu357'
        self.user_one_pw = user_one_pw
        user_one.set_password(user_one_pw)
        user_one.save()
        self.user_one = user_one
        print(f"test_user_exists({user_one.username})")
        print('-'*50)

    def test_user_exists(self):
        user_count = User.objects.all().count()
        print(user_count)
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):
        self.assertTrue(self.user_one.check_password(self.user_one_pw))

