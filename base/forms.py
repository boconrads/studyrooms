from django.forms import ModelForm # import default modelform
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #gives back all fields related to model Room, I will use specific list later