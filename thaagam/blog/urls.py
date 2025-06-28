from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from blog import views

urlpatterns = [
    
    path('',views.home,name="home"),
    path('dashboards',views.dashboard,name="dashboard"),
    path('/register/', views.register, name='register'),
     path('/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

     #part 2
     path('staff_add/', views.staff_create, name='staff_add'),
     path('staff/update/<int:id>/', views.staff_update, name='staff_update'),
      path('staff/delete/<int:id>/', views.staff_delete, name='staff_delete'),
    path('task_add/', views.create_task, name='create_task'),

      path("profile",views.profile,name='profile'),

       path('register-admin/', views.register_admin, name='register_admin'),

       path('pending_users/',views.pending_users,name="pending_users"),
       path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),

     

]
