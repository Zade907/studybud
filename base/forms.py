from django.forms import ModelForm 
from .models import Room 

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  #include all fields from Room model
        exclude = ['host', 'participants']  #exclude host and participants fields