from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def xp_to_next_level(self):
        return (self.level * 200) - self.xp

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.level * 200:
            self.xp -= self.level * 200
            self.level += 1
        self.save()

    def __str__(self):
        return f"{self.user.username} - Level {self.level}"


class Achievement(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.achievement.title}"


class Workout(models.Model):
    DIFFICULTIES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    CATEGORIES = [
        ('workout', 'Workout'),
        ('nutrition', 'Nutrition'),
        ('recovery', 'Recovery'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=200)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTIES)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    xp_value = models.IntegerField(default=0)

    def save(self, *args, **kwargs):

        if self.difficulty == 'easy':
            self.xp_value = 15
        elif self.difficulty == 'medium':
            self.xp_value = 25
        elif self.difficulty == 'hard':
            self.xp_value = 35
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.difficulty}, {self.category})"


class UserWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def complete_workout(self):

        if not self.completed:
            self.completed = True
            profile = self.user.userprofile
            profile.add_xp(self.workout.xp_value)
            self.save()

    def __str__(self):
        return f"{self.user.username} - {self.workout.title} ({'Done' if self.completed else 'Pending'})"
