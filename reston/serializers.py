from django.contrib.auth.models import User, Group
from konferencje.models import Konferencja, Prelegent, Sesja, Zgloszenie
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
        
class PrelegentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prelegent
    
    
class KonferencjaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Konferencja
  
  
class SesjaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sesja
  

class ZgloszenieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Zgloszenie
        
