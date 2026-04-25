from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tracker.models import User, Team, Activity, Workout, Leaderboard


class TeamAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='Test Team',
            description='Test Team Description',
            total_points=100
        )

    def test_get_teams(self):
        """Test retrieving all teams"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_team(self):
        """Test creating a new team"""
        data = {
            'name': 'New Team',
            'description': 'New Team Description',
            'total_points': 0
        }
        response = self.client.post('/api/teams/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='Test Team',
            description='Test Team Description'
        )
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team=self.team,
            total_points=50
        )

    def test_get_users(self):
        """Test retrieving all users"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_user(self):
        """Test creating a new user"""
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'team': self.team.id,
            'total_points': 0
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_get_user_detail(self):
        """Test retrieving a specific user"""
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test User')


class ActivityAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team=self.team
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            description='Morning run',
            duration_minutes=30,
            distance_km=5.0,
            points_earned=50
        )

    def test_get_activities(self):
        """Test retrieving all activities"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_activity(self):
        """Test creating a new activity"""
        data = {
            'user': self.user.id,
            'activity_type': 'walking',
            'description': 'Evening walk',
            'duration_minutes': 20,
            'distance_km': 2.0,
            'points_earned': 30
        }
        response = self.client.post('/api/activities/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 2)


class WorkoutAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team=self.team
        )

    def test_get_workouts(self):
        """Test retrieving all workouts"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_workout(self):
        """Test creating a new workout"""
        data = {
            'user': self.user.id,
            'workout_name': 'Morning Fitness',
            'exercises': {'exercises': [{'name': 'Push-ups', 'sets': 3}]},
            'duration_minutes': 45,
            'calories_burned': 300
        }
        response = self.client.post('/api/workouts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LeaderboardAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team=self.team,
            total_points=100
        )
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            team=self.team,
            rank=1,
            total_points=100,
            total_activities=5
        )

    def test_get_leaderboard(self):
        """Test retrieving leaderboard"""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_leaderboard_read_only(self):
        """Test that leaderboard is read-only"""
        data = {
            'user': self.user.id,
            'team': self.team.id,
            'rank': 1,
            'total_points': 150,
            'total_activities': 6
        }
        response = self.client.post('/api/leaderboard/', data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class APIRootTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_root(self):
        """Test API root endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('workouts', response.data)
        self.assertIn('leaderboard', response.data)

