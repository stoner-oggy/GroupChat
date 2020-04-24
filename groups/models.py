from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

import misaka


# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=256,unique=True)
    description=  models.TextField(blank=True,null=True,)
    description_html = models.TextField(editable=False)
    creation_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    members = models.ManyToManyField(User,through="GroupMember")

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})
    def __str__(self):
        return self.name
    
    class Meta: 
        ordering = ['creation_date']

class GroupMember(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="memberships")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_groups")

    def __str__(self):
        return self.user.name

    class Meta:
        unique_together = ['group','user']

