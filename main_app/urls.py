from django.urls import path
from . import views 

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('workouts/', views.workout_index, name='workout_index'),
     path('workouts/<int:workout_id>/complete/', views.complete_workout, name='complete-workout'),
    path('workouts/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workouts/create/', views.WorkoutCreate.as_view(), name='workout_create'),
    path('workouts/<int:pk>/update/', views.WorkoutUpdate.as_view(), name='workout_update'),
    path('workouts/<int:pk>/delete/', views.WorkoutDelete.as_view(), name='workout_delete')
     
]
