from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, Topic
from django.contrib.auth.models import User
from .forms import RoomForm
from django.db.models import Q #we can wrap search parameters and add & or 'OR' = |
from django.contrib.auth import authenticate, login, logout
#
# rooms = [
#     {'id': 1, 'name': 'lets learn python'},
#     {'id': 2, 'name': 'design with me'},
#     {'id': 3, 'name': 'frontend developers'},
# ]

def loginPage(request): # dont call it login on its own because of built-in function login 
    if request.method == "POST": #checks if the user filled in their info
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username) #checking if the user exists
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password) #need to authenticate if credentials are correct
        if user is not None:
            login(request, user)
            return redirect('home')   
        else:
             messages.error(request, 'Username or password does not exist')


    context = {}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ) #if it contains anything from q (like pyt (fully python)) it will run filter 
    
    
    #rooms = Room.objects.all # this gives you all the rooms that are in the db
    
    topics = Topic.objects.all
    room_count = rooms.count()
    context =  {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk) #returns 1 value, can't be double
    context =  {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') #redirect to home, home is given name
        #print(request.POST) #this and above code is also in django documentation 

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk): #add primary key so we know what we are updating
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #passing instance and prefill with room data

    if request.method == 'POST':
        form= RoomForm(request.POST, instance=room) #tells wich room to update
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form} #dictionary
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk) #we need to know which room we are deleting
    if request.method == 'POST': #when click delete, delete room
        room.delete()
        return redirect('home') #send user back to home after deleting
    return render(request, 'base/delete.html', {'obj': room}) #we are defining the obj as room in this view, obj = name in the template
