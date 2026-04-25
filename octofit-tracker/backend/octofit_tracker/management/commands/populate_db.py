from django.core.management.base import BaseCommand
from tracker.models import User, Team, Activity, Workout, Leaderboard


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Cleared existing data'))

        # Create teams
        marvel_team = Team.objects.create(
            name='Team Marvel',
            description='Marvel Superheroes',
            total_points=0
        )

        dc_team = Team.objects.create(
            name='Team DC',
            description='DC Superheroes',
            total_points=0
        )

        self.stdout.write(self.style.SUCCESS('Created teams'))

        # Create Marvel team users
        marvel_users = [
            {'name': 'Spider-Man', 'email': 'spider-man@marvel.com'},
            {'name': 'Iron Man', 'email': 'iron-man@marvel.com'},
            {'name': 'Captain America', 'email': 'captain-america@marvel.com'},
            {'name': 'Thor', 'email': 'thor@marvel.com'},
            {'name': 'Black Widow', 'email': 'black-widow@marvel.com'},
        ]

        # Create DC team users
        dc_users = [
            {'name': 'Superman', 'email': 'superman@dc.com'},
            {'name': 'Batman', 'email': 'batman@dc.com'},
            {'name': 'Wonder Woman', 'email': 'wonder-woman@dc.com'},
            {'name': 'The Flash', 'email': 'the-flash@dc.com'},
            {'name': 'Green Lantern', 'email': 'green-lantern@dc.com'},
        ]

        users = []

        for user_data in marvel_users:
            user = User.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                team=marvel_team,
                total_points=0
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.name}'))

        for user_data in dc_users:
            user = User.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                team=dc_team,
                total_points=0
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.name}'))

        # Create activities for each user
        activity_types = ['running', 'walking', 'strength_training', 'cycling', 'swimming']
        for idx, user in enumerate(users):
            for i, activity_type in enumerate(activity_types):
                activity = Activity.objects.create(
                    user=user,
                    activity_type=activity_type,
                    description=f'{user.name} doing {activity_type}',
                    duration_minutes=30 + (i * 10),
                    distance_km=5.0 + (i * 0.5) if activity_type in ['running', 'walking', 'cycling'] else None,
                    points_earned=((i + 1) * 10) + (idx * 5)
                )
                user.total_points += activity.points_earned
                self.stdout.write(f'Created activity: {activity.activity_type} for {user.name}')

            user.save()

        self.stdout.write(self.style.SUCCESS('Created activities'))

        # Create workouts for each user
        for user in users:
            workout = Workout.objects.create(
                user=user,
                workout_name=f'{user.name} Morning Fitness',
                exercises={
                    'exercises': [
                        {'name': 'Push-ups', 'sets': 3, 'reps': 10},
                        {'name': 'Squats', 'sets': 3, 'reps': 15},
                        {'name': 'Plank', 'sets': 3, 'duration': 60},
                    ]
                },
                duration_minutes=45,
                calories_burned=300 + (users.index(user) * 50)
            )
            self.stdout.write(f'Created workout: {workout.workout_name}')

        self.stdout.write(self.style.SUCCESS('Created workouts'))

        # Create leaderboard entries
        rank = 1
        for user in sorted(users, key=lambda u: u.total_points, reverse=True):
            leaderboard_entry = Leaderboard.objects.create(
                user=user,
                team=user.team,
                rank=rank,
                total_points=user.total_points,
                total_activities=Activity.objects.filter(user=user).count()
            )
            self.stdout.write(f'Created leaderboard entry: {user.name} - Rank {rank}')
            rank += 1

        self.stdout.write(self.style.SUCCESS('Created leaderboard entries'))

        # Update team total points
        for team in [marvel_team, dc_team]:
            team.total_points = sum(User.objects.filter(team=team).values_list('total_points', flat=True))
            team.save()

        self.stdout.write(self.style.SUCCESS(self.style.SUCCESS('Database population completed successfully!')))
