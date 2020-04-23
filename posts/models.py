from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


import misaka

from groups.models import Group

User = get_user_model()



# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs) # Call the real save() method
    
    def get_absolute_url(self):
        return reverse("posts:single", kwargs={"username":self.user.username, "pk": self.pk})

        
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','message']
