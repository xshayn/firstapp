from django.urls import path
from .views import TaskList, TaskDelete, TaskCreate, TaskDetail, TaskUpdate, TaskLogin, RegisterForm
from django.contrib.auth.views import LogoutView

urlpatterns= [
    path("tasklist/", TaskList.as_view(),name="tasklist"),
    path("taskdelete/<int:pk>/", TaskDelete.as_view(),name="taskdelete"),
    path("taskcreate/", TaskCreate.as_view(),name="taskcreate"),
    path("taskdetail/<int:pk>/", TaskDetail.as_view(),name="taskdetail"),
    path("taskupdate/<int:pk>/", TaskUpdate.as_view(),name="taskupdate"),
    path("", TaskLogin.as_view(),name="login"),
    path("register/", RegisterForm.as_view(),name="register"),
    path("logout/", LogoutView.as_view(next_page="login"),name="logout"),

]