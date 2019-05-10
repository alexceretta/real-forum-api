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
    avatar_url = serializers.SerializerMethodField('get_image_url')

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

class ThreadListSerializer(serializers.ModelSerializer):
    """
    Serializer for Thread model (for listing)
    """
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_details = UserSerializer(many=False, read_only=True, source="user")
    lastUser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Thread
        fields = "__all__"

class ThreadPostSerializer(serializers.Serializer):
    """
    Serializer for Thread and Post models for CREATE methods
    """
    title = serializers.CharField(required=True, max_length=255)
    message = serializers.CharField(max_length=None,required=True)
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    def create(self, validated_data):
        thread = Thread.objects.create_new_thread(**validated_data)
        return thread

class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializer for Thread model
    """
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    board_details = BoardSerializer(many=False, read_only=True, source="board")
    user = UserSerializer(many=False, read_only=True)
    lastUser = UserSerializer(many=False, read_only=True)

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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_details = UserSerializer(many=False, read_only=True, source="user")

    class Meta:
        model = Post
        fields = '__all__'