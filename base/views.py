from django.shortcuts import render
from .models import Room

rooms = [
    {'id': 1, 'name': 'Lets study python'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Frontend developers'},
]

# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = {'rooms' : rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    for i in rooms:
        if i["id"] == int(pk):
            room = i
    context = {'room' : room}

    return render(request, 'base/room.html',context)