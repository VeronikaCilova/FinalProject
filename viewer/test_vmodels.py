from django.test import TestCase
from viewer.models import *


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.position = Position.objects.create(position='CFO', department='Finance')
        self.profile = Profile.objects.create(
            user=self.user,
            position=self.position,
            picture=None,
            supervisor=None,
            bio='This is a test bio.'
        )

    def test_profile_creation(self):
        self.assertTrue(Profile.objects.exists())
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.position.position, 'CFO')


class TodoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.position = Position.objects.create(position='IT manager', department='IT')
        self.profile = Profile.objects.create(
            user=self.user,
            position=self.position,
            picture=None,
            supervisor=None,
            bio='This is a test bio.'
        )
        self.todo = Todo.objects.create(
            title='Test Todo',
            details='Test Details',
            date='2024-01-01',
            profile=self.profile
        )

    def test_todo_creation(self):
        self.assertTrue(Todo.objects.exists())
        self.assertEqual(self.todo.title, 'Test Todo')

    def test_str_method(self):
        self.assertEqual(str(self.todo), 'Test Todo')


class FeedbackModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.position = Position.objects.create(position='Cleaning Lady', department='Maintanance')
        self.profile1 = Profile.objects.create(
            user=self.user,
            position=self.position,
            picture=None,
            supervisor=None,
            bio='This is a test bio.'
        )
        self.profile2 = Profile.objects.create(
            user=self.user,
            position=self.position,
            picture=None,
            supervisor=self.profile1,
            bio='This is another test bio.'
        )
        self.feedback = Feedback.objects.create(
            evaluator=self.profile1,
            subject_of_review=self.profile2,
            description='Test Feedback'
        )

    def test_feedback_creation(self):
        self.assertTrue(Feedback.objects.exists())
        self.assertEqual(self.feedback.description, 'Test Feedback')

    def test_str_method(self):
        self.assertEqual(str(self.feedback), f"{self.profile2} ({self.feedback.creation_date})")
