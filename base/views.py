from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

#
# rooms = [
#     {'id': 1, 'name': 'lets learn python'},
#     {'id': 2, 'name': 'design with me'},
#     {'id': 3, 'name': 'frontend developers'},
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(topic__name__icontains=q) #if it contains anything from q (like pyt (fully python)) it will run filter 
    #rooms = Room.objects.all # this gives you all the rooms that are in the db
    
    topics = Topic.objects.all 
    context =  {'rooms': rooms, 'topics': topics}
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
