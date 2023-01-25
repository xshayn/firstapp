from django.shortcuts import render,  redirect
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from .models import Task
from django.views.generic.edit import DeleteView, CreateView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin






class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'task'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["task"] = context["task"].filter(user=self.request.user, title__icontains= search_input)
        else:
            context["task"] = context["task"].filter(user=self.request.user)
        context["count"] = context["task"].filter(complete=False).count()
        context["search_input"] = search_input
        return context

class TaskDelete( LoginRequiredMixin, DeleteView):
    model = Task
    fields=["title", "description", "complete"]
    success_url = reverse_lazy("tasklist")



class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "complete"]
    success_url= reverse_lazy("tasklist")
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "complete"]
    success_url= reverse_lazy("tasklist")
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskUpdate, self).form_valid(form)


class TaskDetail( LoginRequiredMixin, DetailView):
    model = Task

class TaskLogin(LoginView):
    model= Task
    success_url= reverse_lazy("tasklist")
    template_name= "todo/login.html"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy("tasklist")



class RegisterForm(FormView):
    model = Task
    form_class = UserCreationForm
    template_name= "todo/register.html"
    redirect_authenticated_user= True
    success_url= reverse_lazy("tasklist") 
    def form_valid(self, form):
        user = form.save()     
        if user is not None:
          login(self.request , user)

        return super(RegisterForm, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("tasklist")
        return super(RegisterForm, self).get(*args, **kwargs)




