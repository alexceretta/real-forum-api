"""
Serializer module
"""
from datetime import datetime

from rest_framework import serializers
from foro_user.models import User, Thread, Board, Post

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    avatar_url = serializers.SerializerMethodField('get_image_url');

    class Meta:
        model = User
        fields = ('id', 'auth0Id', 'name', 'email', 'birthDate', 'avatar', 'title',
                  'registrationDate', 'avatar_url')

    def update(self, instance, validated_data):        
        instance.birthDate = validated_data.get('birthDate', instance.birthDate)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

    def get_image_url(self, obj):        
        if obj.avatar:
            request = self.context.get('request')            
            return request.build_absolute_uri(obj.avatar.url)
        else:
            return ""

class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for Board model
    """
    class Meta:
        model = Board
        fields = '__all__'
        depth=0

class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializer for Thread model
    """
    board = BoardSerializer(many=False)
    user = UserSerializer(many=False)
    lastUser = UserSerializer(many=False)

    class Meta:
        model = Thread
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.lastUser = validated_data.get('lastUser', instance.lastUser)
        instance.updateDate = datetime.now()        
        instance.save()
        return instance

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model
    """
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all())
    user = UserSerializer(many=False)

    class Meta:
        model = Post
        fields = '__all__'