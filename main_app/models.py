from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.user.username} - Level {self.level}"

    def xp_to_next_level(self):
        return (self.level * 200) - self.xp

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.level * 200:
            self.xp -= self.level * 200
            self.level += 1
        self.save()


class Workout(models.Model):

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=300, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTIES)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    xp_value = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.difficulty}, {self.category})"


class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    users = models.ManyToManyField(User, related_name="achievements", blank=True)

    def __str__(self):
        return self.title

    @staticmethod
    def award(title, description, user):
        achievement, _ = Achievement.objects.get_or_create(
        title=title, defaults={"description": description})
        achievement.users.add(user)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        Achievement.objects.create(
            profile=profile,
            title="Welcome!",
            description="You joined the fitness app and created your profile!"
        )
        