from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import Topic, TopicRequest
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

def redirect_home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('superuser_home')
        return redirect('user_home')
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('superuser_home')
            return redirect('user_home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html', {})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_home(request):
    if request.user.is_superuser:
        return redirect('superuser_home')
    if request.method == 'POST':
        topic_name = request.POST.get('topic_name')
        partitions = request.POST.get('partitions', 1)
        TopicRequest.objects.create(
            topic_name=topic_name,
            partitions=partitions,
            requested_by=request.user
        )
        return redirect('user_home')
    requests = TopicRequest.objects.filter(requested_by=request.user)
    return render(request, 'user_home.html', {'requests': requests})

@login_required
def superuser_home(request):
    if not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=403)
    requests = TopicRequest.objects.all()
    return render(request, 'superuser_home.html', {'requests': requests})

@login_required
@csrf_exempt
def create_topic(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            topic_name = data.get('topic_name')
            partitions = data.get('partitions', 1)
            Topic.objects.create(
                name=topic_name,
                creator=request.user,
                partitions=partitions
            )
            return HttpResponse('Topic created', status=200)
        except Exception as e:
            return HttpResponse(str(e), status=400)
    return HttpResponse('Method not allowed', status=405)

@login_required
def handle_request(request, request_id):
    if not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=403)
    topic_request = TopicRequest.objects.get(id=request_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        topic_request.status = action
        topic_request.reviewed_by = request.user
        topic_request.reviewed_at = timezone.now()
        topic_request.save()
        if action == 'Approved':
            Topic.objects.create(
                name=topic_request.topic_name,
                creator=topic_request.requested_by,
                partitions=topic_request.partitions
            )
        return redirect('superuser_home')
    return render(request, 'handle_request.html', {'request': topic_request})

@login_required
@csrf_exempt
def create_partition(request, topic_name):
    if not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=403)
    try:
        topic = Topic.objects.get(name=topic_name)
        topic.partitions += 1
        topic.save()
        return HttpResponse('Partition added', status=200)
    except Topic.DoesNotExist:
        return HttpResponse('Topic not found', status=404)

@login_required
@csrf_exempt
def delete_partition(request, topic_name):
    if not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=403)
    try:
        topic = Topic.objects.get(name=topic_name)
        if topic.partitions > 1:
            topic.partitions -= 1
            topic.save()
            return HttpResponse('Partition removed', status=200)
        return HttpResponse('Cannot reduce partitions below 1', status=400)
    except Topic.DoesNotExist:
        return HttpResponse('Topic not found', status=404)

@login_required
def topic_detail(request, topic_name):
    try:
        topic = Topic.objects.get(name=topic_name)
        return render(request, 'topic_detail.html', {'topic': topic})
    except Topic.DoesNotExist:
        return HttpResponse('Topic not found', status=404)