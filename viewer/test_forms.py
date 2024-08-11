import datetime

from django.test import TestCase

from viewer.models import *
from viewer.views import ReviewForm, GoalForm


class ReviewFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        goal = Goal.objects.create(
            profile_id=2,
            name='Random name2',
            description='Detailed description2',
            deadline=datetime.date(year=2026, month=1, day=25),
            priority='Highest priority2',
            status='Defined status2'
        )
        profile = Profile.objects.create(
            user_id=1,
            picture=None,
            position=Position.objects.create(position='Manager', department='Fleet'),
            supervisor=Profile.objects.create(user=User.objects.create(
                username='Marek Supervisor',
                email='marek.supervisor@firma.cz',
                password='nereknu987')),
            bio='Profile biography'
        )
        goal.profile = profile
        goal.save()

    def test_review_form_is_valid(self):
        goal = Goal.objects.get(id=1)
        form = ReviewForm(
            data={'goal': goal.id,
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
        profile = Profile.objects.create(
            user=User.objects.create(
                username='testuser',
                first_name='noname',
                last_name='tester',
                email='testuser@firma.cz',
                password='password'
            ),
            picture=None,
            position=Position.objects.create(position='Manager', department='Fleet'),
            supervisor=Profile.objects.create(user=User.objects.create(
                username='Marek Supervisor',
                first_name='Marek',
                last_name='Supervisor',
                email='marek.supervisor@firma.cz',
                password='nereknu987')),
            bio='Profile biography'
        )

    def test_goal_form_is_valid(self):
        profile = Profile.objects.get(id=2)
        form = GoalForm(
            data={'profile': profile.id,
                  'name': 'Test goal',
                  'description': 'this is a lowercase test description.',
                  'deadline': '2025-01-20',
                  'priority': 'low',
                  'status': 'doing',
                  }
        )
        print(f"test_goal_form_is_valid({form.data})")
        self.assertTrue(form.is_valid())

    def test_goal_form_no_data(self):
        form = GoalForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_goal_form_is_not_valid_deadline(self):
        profile = Profile.objects.get(id=2)
        form = GoalForm(
            data={'profile': profile.id,
                  'name': 'Test goal',
                  'description': 'this is a lowercase test description.',
                  'deadline': '2023-12-31',     # invalid deadline (past)
                  'priority': 'low',
                  'status': 'doing',
                  }
        )
        print(f"test_goal_form_is_not_valid({form.data})")
        self.assertFalse(form.is_valid())
