from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ToDoListItem(models.Model):
    creator = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    content = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.content

