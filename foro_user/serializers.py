"""
Serializer module
"""
from rest_framework import serializers
from foro_user.models import User, Thread

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = ('id', 'auth0Id', 'name', 'email', 'birthDate', 'avatar', 'title',
                  'registrationDate')

    def update(self, instance, validated_data):
        instance.birthDate = validated_data.get('birthDate', instance.birthDate)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializer for Thread model
    """
    class Meta:
        model = Thread
        fields = ('title', 'board', 'user', 'lastUser', 'updateDate', 'postCount')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
