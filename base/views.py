from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm,UserForm


def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist")

    context = {"page": page}

    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = UserCreationForm()
    context = {"form": form}

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()

    roomMessages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {"rooms": rooms, "topics": topics, "room_count": room_count,"roomMessages":roomMessages}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        body = request.POST.get("body")
        roomMessage = Message.objects.create(room=room, body=body, user=request.user)
        roomMessage.save()
        room.participants.add(request.user)
        return redirect("room", pk=room.id)

    context = {"room": room, "roomMessages": roomMessages, "participants": participants}
    return render(request, "base/room.html", context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    roomMessages = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user":user,"rooms":rooms,"roomMessages":roomMessages,"topics":topics}
    return render(request,"base/profile.html",context)

@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        
        return redirect("home")
    topics = Topic.objects.all()
    context = {"form": form,"topics":topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect("home")
    topics = Topic.objects.all()
    context = {"form": form,"topics":topics,"room":room}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})

@login_required(login_url="login")
def deleteMessage(request, pk):
    roomMessage = Message.objects.get(id=pk)

    if request.user != roomMessage.user:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        roomMessage.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": roomMessage})

@login_required(login_url="login")
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect("user-profile",pk=user.id)

    context = {"form":form}
    return render(request,'base/update_profile.html',context)

def topicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    room_count = Room.objects.all().count()
    context = {"topics":topics,"room_count":room_count}
    return render(request,'base/topics.html',context)

def activityPage(request):
    roomMessages = Message.objects.all()
    context = {"roomMessages":roomMessages}
    return render(request,'base/activity.html',context)