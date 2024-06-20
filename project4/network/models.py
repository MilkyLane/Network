from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posting, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    profile_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')


User.add_to_class('follower_count', property(lambda u: Follow.objects.filter(profile_user=u).count()))
User.add_to_class('following_count', property(lambda u: Follow.objects.filter(user=u).count()))