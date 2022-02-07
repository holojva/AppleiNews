from re import A
from django.db import models
from django.conf import settings
from datetime import datetime
# Create your models here.
User = settings.AUTH_USER_MODEL
class Likes(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    like = models.BooleanField(default=False)
class Commentaries(models.Model):
    class Meta:
        ordering = ['-date']

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(datetime.now(), null=True)
    text = models.TextField(blank=False, null=True)

class News(models.Model) :
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    article = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    commentary = models.ManyToManyField(Commentaries)
    likes = models.ManyToManyField(Likes)
    def __str__(self) :
        return self.article
    def get_likes(self):
        return self.likes.count


