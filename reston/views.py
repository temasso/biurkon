# Create your views here.
from django.contrib.auth.models import User, Group
from konferencje.models import Konferencja, Sesja, Prelegent, Zgloszenie
from rest_framework import viewsets
from reston.serializers import UserSerializer, GroupSerializer, PrelegentSerializer, KonferencjaSerializer, SesjaSerializer, ZgloszenieSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
    
       
class PrelegentViewSet(viewsets.ModelViewSet):
    
    queryset = Prelegent.objects.all()
    serializer_class = PrelegentSerializer
     
    
    
class KonferencjaViewSet(viewsets.ModelViewSet):
    queryset = Konferencja.objects.all()
    serializer_class = KonferencjaSerializer
  
  
class SesjaViewSet(viewsets.ModelViewSet):
    queryset = Sesja.objects.all()
    serializer_class = SesjaSerializer
  

class ZgloszenieViewSet(viewsets.ModelViewSet):
    queryset = Zgloszenie.objects.all()
    serializer_class = ZgloszenieSerializer
    
        