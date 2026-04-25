from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from tracker.models import User, Team, Activity, Workout, Leaderboard
from tracker.serializers import (
    UserSerializer,
    TeamSerializer,
    ActivitySerializer,
    WorkoutSerializer,
    LeaderboardSerializer
)


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint that lists all available endpoints
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'teams': reverse('team-list', request=request, format=format),
        'activities': reverse('activity-list', request=request, format=format),
        'workouts': reverse('workout-list', request=request, format=format),
        'leaderboard': reverse('leaderboard-list', request=request, format=format),
    })


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['total_points', 'name', 'created_at']
    ordering = ['-total_points']


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['total_points', 'name', 'created_at']
    ordering = ['-total_points']


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__name', 'activity_type', 'description']
    ordering_fields = ['points_earned', 'duration_minutes', 'created_at']
    ordering = ['-created_at']


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Workouts
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__name', 'workout_name']
    ordering_fields = ['calories_burned', 'duration_minutes', 'created_at']
    ordering = ['-created_at']


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing Leaderboard (Read-only)
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__name', 'team__name']
    ordering_fields = ['rank', 'total_points']
    ordering = ['rank']

