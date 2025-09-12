from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.redirect_home, name='home'),
    path('home/', views.redirect_home, name='redirect_home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_home/', views.user_home, name='user_home'),
    path('superuser_home/', views.superuser_home, name='superuser_home'),
    path('create_topic/', views.create_topic, name='create_topic'),
    path('handle_request/<int:request_id>/', views.handle_request, name='handle_request'),
    path('create_partition/<str:topic_name>/', views.create_partition, name='create_partition'),
    path('delete_partition/<str:topic_name>/', views.delete_partition, name='delete_partition'),
    path('topic/<str:topic_name>/', views.topic_detail, name='topic_detail'),
]