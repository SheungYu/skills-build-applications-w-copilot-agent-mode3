from django.contrib import admin
from tracker.models import User, Team, Activity, Workout, Leaderboard


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_points', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-total_points']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'team', 'total_points', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['team', 'created_at']
    ordering = ['-total_points']
    readonly_fields = ['created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'duration_minutes', 'points_earned', 'created_at']
    search_fields = ['user__name', 'activity_type']
    list_filter = ['activity_type', 'created_at']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout_name', 'duration_minutes', 'calories_burned', 'created_at']
    search_fields = ['user__name', 'workout_name']
    list_filter = ['created_at']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'rank', 'total_points', 'total_activities', 'updated_at']
    search_fields = ['user__name', 'team__name']
    list_filter = ['team', 'rank']
    ordering = ['rank']
    readonly_fields = ['updated_at']

