from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin

from . import models


# Create your views here.

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    model = models.Group
    fields = ['name','description']

class SingleGroup(generic.DetailView):
    model = models.Group

class ListGroups(generic.ListView):
    model = models.Group
    template_name = "groups/group_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(models.Group,slug=self.kwargs.get('slug'))
        try:
            models.GroupMember.objects.create(user=self.request.user,group = group)
        except :
            messages.warning(self.request,('warning already a member'))
        else:
            messages.success(self.request,"you are a new member")
        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    def get(self, request, *args, **kwargs):
    
        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
