from rest_framework import serializers
from tracker.models import User, Team, Activity, Workout, Leaderboard


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'total_points', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'team', 'team_name', 'total_points', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'user', 'user_name', 'activity_type', 'description', 'duration_minutes', 'distance_km', 'points_earned', 'created_at']


class WorkoutSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'user', 'user_name', 'workout_name', 'exercises', 'duration_minutes', 'calories_burned', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'user_name', 'team', 'team_name', 'rank', 'total_points', 'total_activities', 'updated_at']
