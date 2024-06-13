
from rest_framework import serializers
from accounts.models import UserAccount

class UserAccountSerialiser(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        exclude = ['password'] 
       
