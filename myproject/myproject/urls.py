from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('', views.login_view, name='root'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('home/', views.redirect_home, name='home'),
    path('user_home/', views.user_home, name='user_home'),
    path('superuser_home/', views.superuser_home, name='superuser_home'),
    path('home/<str:topic_name>/', views.topic_detail, name='topic_detail'),

    # Topic operations
    path('create_topic/', views.create_topic, name='create_topic'),
    path('create_partition/<str:topic_name>/', views.create_partition, name='create_partition'),
    path('delete_partition/<str:topic_name>/', views.delete_partition, name='delete_partition'),

    # Topic requests (Superuser actions)
    path('handle_request/<int:request_id>/', views.handle_request, name='handle_request'),
]