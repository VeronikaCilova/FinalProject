from django.test import TestCase
from viewer.models import *
import datetime


class GoalModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='Kate Moss',
            first_name='Kate',
            last_name='Moss',
            email='kate.moss@firma.cz',
            password='password'
        )
        goal = Goal.objects.create(
            profile_id=1,
            name='Random name',
            description='Detailed description',
            deadline=datetime.date(year=2025, month=10, day=5),
            priority='Highest priority',
            status='Defined status'
        )
        profile = Profile.objects.create(
            user_id=1,
            picture=None,
            position=Position.objects.create(position='Manager', department='Fleet'),
            supervisor=Profile.objects.create(user=User.objects.create(username='Marek Supervisor', email='marek.supervisor@firma.cz', password='nereknu987')),
            bio='Profile biography'
        )
        profile.user = user
        goal.profile = profile
        goal.save()

    def setUp(self):
        print('-'*50)

    def test_goal_str(self):
        goal = Goal.objects.get(id=1)
        print(f"test_goal_str: {goal}")
        self.assertEqual(goal.__str__(), "Random name (2025-10-05)")

    def test_goal_profile(self):
        goal = Goal.objects.get(id=1)
        print(f"test_profile: {goal.profile}")
        self.assertEqual(goal.profile.__str__(), "Kate Moss")

    def test_priority(self):
        goal = Goal.objects.get(id=1)
        print(f"test_priority: {goal.priority}")
        self.assertEqual(goal.priority.__str__(), "Highest priority")

    def test_status(self):
        goal = Goal.objects.get(id=1)
        print(f"test_status: {goal.status}")
        self.assertEqual(goal.status.__str__(), "Defined status")


class ReviewModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        review = Review.objects.create(
            description='Review comment',
            evaluator=Profile.objects.create(user=User.objects.create(
                username='Bobba Fett',
                email='bobba.fett@firma.cz',
                password='nereknu654')),
            subject_of_review=Profile.objects.create(user=User.objects.create(
                username='Leia Organa',
                email='leia.organa@firma.cz',
                password='nereknu432')),
            goal='Long term goal',
            training='Suggested training'
        )
        review.save()

    def setUp(self):
        print('-' * 50)

    def test_review_description(self):
        review = Review.objects.get(id=1)
        print(f"test_description: {review.description}")
        self.assertEqual(review.description.__str__(), "Review comment")

    def test_review_goal(self):
        review = Review.objects.get(id=1)
        print(f"test_goal: {review.goal}")
        self.assertEqual(review.goal.__str__(), "Long term goal")

    def test_review_training(self):
        review = Review.objects.get(id=1)
        print(f"test_training: {review.training}")
        self.assertEqual(review.training.__str__(), "Suggested training")

    def test_evaluator_exists(self):
        review = Review.objects.get(id=1)
        print(f"test_evaluator: {review.evaluator}")
        self.assertTrue(Profile.objects.exists())
