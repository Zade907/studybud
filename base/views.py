from django.shortcuts import render, redirect 
from django.db.models import Q #importing Q object for complex queries
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User #importing user model
from django.contrib import messages #for flash messages
from django.contrib.auth import authenticate, login, logout #importing authentication functions
from .models import Room,Topic, Message
from .forms import RoomForm #importing RoomForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# rooms = [
#     {'id': 1, 'name': 'Lets study python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]
# ]

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower() #get username from the html form 
        password = request.POST.get('password') #get password from the html form

        try:
            user = User.objects.get(username = username) #check if user exists
        except:
            messages.error(request, 'User does not exist')  #display error message if user does not exist
        
        user = authenticate(request, username = username, password = password) #authenticate user

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')
        
    context = {'page': page}
    return render(request, 'base/login_register.html', context )

def LogoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
    else:
        messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html',{'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q)|
        Q(description__icontains = q)
        )  #get all rooms from db with the query parameter

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))

    context = {'rooms' : rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk) #get room with specific id 
    room_messages = room.message_set.all()  #get all messages related to that room
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user  = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)
    context = {'room_messages' : room_messages, 'room': room, 'participants': participants}
    return render(request, 'base/room.html',context)

@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit = False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url = 'login')
def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url = 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    context = {'obj': room}

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)

@login_required(login_url = 'login')
def deleteMessage(request,pk):
    message = Message.objects.get(id = pk)
    context = {'obj' : message}

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk = message.room.id)
    return render(request, 'base/delete.html', context)


def UserProfile(request, pk):
    user = User.objects.get(id = pk)
    room = user.room_set.all()
    room_messages = user.message_set.all()  
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': room, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)