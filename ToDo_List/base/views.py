from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin #add this mixin where I want to restrict the user


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    # it will redirect the authenticated users to direct tasks page
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin,ListView):
    model = Task 
    context_object_name = "tasks"


class TaskDetails(LoginRequiredMixin,DetailView):
    model = Task 
    context_object_name = "task"
    template_name = 'base/task_details.html'   


class TaskCreate(CreateView):
    """Create view will create fields automatically using the model task"""
    model = Task
    fields = '__all__'
    #Send user back to main list of tasks
    success_url = reverse_lazy('tasks')


class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
