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




class Home(LoginView):
    template_name = 'home.html'

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


def Workout_index(request):
    return render(request, 'workouts_index.html', {'workout': Workout})


def dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    workouts = Workout.objects.filter(userprofile = profile).order_by('difficulty')
    achievements = Achievement.objects.filter(user=request.user).order_by('title')

    xp_needed = profile.level * 200
    progress = round((profile.xp / xp_needed) * 200, 1) if xp_needed else 0
    total_xp = f"{profile.xp} / {xp_needed}"
  

    return render(request, 'dashboard.html', {
        'profile': profile,
        'workouts': workouts,
        'achievements': achievements,
        'progress': progress,
        'total_xp': total_xp
       
    })

# def workout_index(request):
#     workouts= Workout.objects.filter(user_id = UserProfile)
#     return render(request, 'workout_index.html', {'workouts': workouts})

def workout_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    return render(request, 'workout_detail.html', {'workout': workout})

def complete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, userprofile__user=request.user)
    profile = workout.userprofile

    if not workout.completed:
        workout.completed = True
        workout.save()
        xp_gain = {'easy': 10, 'medium': 25, 'hard': 40}.get(workout.difficulty, 15)
        profile.xp += xp_gain

        # Level up logic
        xp_needed = profile.level * 200
        if profile.xp >= xp_needed:
            profile.xp -= xp_needed
            profile.level += 1

        profile.save()

        # Give achievement for first completed workout
    if not Achievement.objects.filter(user=request.user, title="First Workout!").exists():
        Achievement.objects.create(
        user=request.user,
        title="First Workout!",
        description="Completed your first workout!"
    )

class WorkoutCreate(CreateView):
    model = Workout
    fields = ['title', 'description', 'difficulty', 'category']
    template_name = 'workouts/workout_form.html'
    success_url ='dashboard/'

    def form_valid(self, form):
        profile = UserProfile.objects.get(user=self.request.user)
        form.instance.userprofile = profile
        return super().form_valid(form)


class WorkoutUpdate(UpdateView):
    model = Workout
    fields = ['title', 'description', 'difficulty', 'category', 'completed']
    template_name = 'workouts/workout_form.html'
    success_url ='dashboard/'


class WorkoutDelete(DeleteView):
    model = Workout
    template_name = 'workouts/workout_confirm_delete.html'
    success_url ='dashboard/'