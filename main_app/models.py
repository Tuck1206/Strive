from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def xp_to_next_level(self):
        return (self.level * 100) - self.xp
   
    def add_xp(self, amount):
        self.xp += amount 
        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            self.save()

def __str__(self):
    return f"{self.user.username} - level {self.level}"

class Achievement(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=200)
    
def __str__(self):
    return self.title

class UserAchievement(models.model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

class Workout(models.Model):
    DIFFICULTIES = [
        ('easy' , 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    CATEGORIES = [
        ('workout', 'Workout'),
        ('nutrition', 'Nutrition'),
        ('recovery', 'Recovery')
    ]

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=200)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTIES)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    xp_vaule = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.difficulty}, {self.category})" 
    
class UserWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    def complete(self):
        if not self.complete:
            self.complete = True
            self.user.userprofile.add.xp(self.workout.xp_vaule)
            self.save()
