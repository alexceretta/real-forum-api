import foro_user.models
from django.db import models


class ThreadManager(models.Manager):
    """
    Manager class to handle special thread functions
    """

    def create_new_thread(self, board, user, title, message):
        """
        Creates a new Thread and its initial Post
        """
        print('{} - {} - {} - {}'.format(board, user, title, message))
        # Saves the Thread first
        thread = foro_user.models.Thread(
            title=title,
            board=board,
            user=user,
            lastUser=user
        )
        thread.save()
        # Uses saved Thread to create the post
        post = foro_user.models.Post(
            message=message,
            thread=thread,
            user=user
        )
        post.save()
        return thread
