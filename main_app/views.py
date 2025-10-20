from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Workout, UserProfile, Achievement
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin




def home(request):
    return HttpResponse('<h1>Welcome to Strive!</h1>')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid sign up — try again.'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


def dashboard(request):
    profile = UserProfile.objects.get(id=request.user.id)
    workouts = Workout.objects.filter(user=request.user).order_by('difficulty')
    achievements = Achievement.objects.filter(user=request.user).order_by('difficulty')
    xp_needed = profile.level * 200
    progress = round((profile.xp / xp_needed) * 200, 1) if xp_needed else 0

    return render(request, 'dashboard.html', {
        'profile': profile,
        'workouts': workouts,
        'achievements': achievements,
        'progress': progress,
    })

def workout_index(request):
    workouts= Workout.objects.filter(user=request.user)
    return render(request, 'workouts_index.html', {'workouts': workouts})

def workout_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    return render(request, 'workouts_detail.html', {'workout': workout})

def complete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    workout.complete_workout()  
    return redirect('workout_index.html')

class WorkoutCreate(CreateView):
    model = Workout
    fields = ['title', 'description', 'difficulty', 'category']
    template_name = 'workout_form.html'
    success_url ='workouts/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WorkoutUpdate(UpdateView):
    model = Workout
    fields = ['title', 'description', 'difficulty', 'category', 'completed']
    template_name = 'workout_form.html'
    success_url ='workouts/'


class WorkoutDelete(DeleteView):
    model = Workout
    template_name = 'workout_confirm_delete.html'
    success_url ='workouts/'