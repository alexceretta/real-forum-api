"""
Module containing all Models related to the USER part of the project
"""
from django.db import models
from foro_user.modelManagers import ThreadManager

class User(models.Model):
    """
    Main User class
    """
    auth0Id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    birthDate = models.DateField()
    avatar = models.ImageField(upload_to="avatars", null=True)
    title = models.CharField(max_length=50, default="New User")
    registrationDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)

class Board(models.Model):
    """
    Main Board class
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

class Thread(models.Model):
    """
    Main Thread class
    """
    title = models.CharField(max_length=255)
    board = models.ForeignKey("Board", related_name="threads", on_delete=models.CASCADE)
    user = models.ForeignKey("User", related_name="+", on_delete=models.PROTECT)
    lastUser = models.ForeignKey("User", related_name="+", null=True, on_delete=models.PROTECT)
    creationDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now_add=True)
    postCount = models.IntegerField(default=1)

    objects = ThreadManager()

    class Meta:
        ordering = ("updateDate",)

class Post(models.Model):
    """
    Main Post class
    """
    message = models.TextField()
    thread = models.ForeignKey(Thread, related_name="posts", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    creationDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now_add=True)