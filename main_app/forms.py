from django import forms
from .models import UserProfile, Workout

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'xp', 'level']
        widgets = {
            'xp': forms.NumberInput(attrs={'readonly': True}),
            'level': forms.NumberInput(attrs={'readonly': True}),
        }


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['title', 'description', 'difficulty', 'category']
