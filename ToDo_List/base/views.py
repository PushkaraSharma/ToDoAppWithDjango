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
 
    def get_context_data(self, **kwargs):
        """here we want to modify the data so that only user can see his data, not all the tasks of every user"""
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        # getting the number of unfinsihed tasks
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


class TaskDetails(LoginRequiredMixin,DetailView):
    model = Task 
    context_object_name = "task"
    template_name = 'base/task_details.html'   


class TaskCreate(LoginRequiredMixin,CreateView):
    """Create view will create fields automatically using the model task"""
    model = Task
    fields = ['title','description','complete']
    #Send user back to main list of tasks
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
