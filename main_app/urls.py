from django.urls import path
from . import views 

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('workouts/', views.Workout_index, name='workout_index'),
    path('complete/<int:workout_id>/', views.complete_workout, name='complete_workout'),
    path('workouts/<int:workout_id>/', views.workout_detail, name='workout_detail.html'),
    path('workouts/create/', views.WorkoutCreate.as_view(), name='workout_create'),
    path('workouts/<int:pk>/update/', views.WorkoutUpdate.as_view(), name='workout_update'),
    path('workouts/<int:pk>/delete/', views.WorkoutDelete.as_view(), name='workout_delete')
     
]
