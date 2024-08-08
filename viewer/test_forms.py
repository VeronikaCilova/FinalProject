from django.test import TestCase

from viewer.models import *
from viewer.views import ReviewForm, GoalForm

from datetime import date


class ReviewFormTest(TestCase):
    def test_review_form_is_valid(self):
        form = ReviewForm(
            data={'goal': 'Test something',
                  'description': 'Test description',
                  'training': 'Test training'
                  }
        )
        print(f"test_review_form_is_valid({form.data})")
        self.assertTrue(form.is_valid())

    def test_review_form_no_data(self):
        form = ReviewForm(data={})
        self.assertTrue(form.is_valid())


class GoalFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.profile = Profile.objects.create(
            user=User.objects.create(
                username='testuser',
                email='testuser@firma.cz',
                password='password'
            ),
            picture=None,
            position=Position.objects.create(position='Manager', department='Fleet'),
            supervisor=Profile.objects.create(user=User.objects.create(
                username='Marek Supervisor',
                email='marek.supervisor@firma.cz',
                password='nereknu987')),
            bio='Profile biography'
        )

    def test_goal_form_is_valid(self):
        form = GoalForm(
            data={'profile': self.profile.user.username,
                  'name': 'Test name',
                  'description': 'this is a lowercase test description.',
                  'deadline': date.today(),
                  'priority': 'Test priority',
                  'status': 'Test status',
                  }
        )
        print(f"test_goal_form_is_valid({form.data})")
        self.assertTrue(form.is_valid())

    def test_goal_form_no_data(self):
        form = GoalForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

