from django import forms
from .models import Workout, UserProfile

class WorkoutForm(forms.ModelForm):
    class meta:
        model = Workout
        fields = ["title", "difficulty", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "difficulty": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"})
        }


class UserProfileForm(forms.ModelForm):
    class meta:
        model = UserProfile
        fields = ["user", "level", "xp"]
        widgets = {
            "user": forms.HiddenInput(),
            "level": forms.NumberInput(attrs={"class": "form-control"}),
            "xp": forms.NumberInput(attrs={"class": "form-control"})
        }