"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from  todo import views

urlpatterns = [
    path('', views.home,name='home'),
    path('admin/', admin.site.urls),
    #AUTH
    path('signup/',views.signupuser,name='signupuser'),
    path('logout/',views.logoutUser,name='logoutUser'),
    path('login/',views.loginuser,name='loginuser'),
    #TODO
    path('create/',views.createTodo,name='createTodo'),
    path('todo/<int:todo_pk>',views.viewTodo,name='viewTodo'),
    path('todo/<int:todo_pk>/complete',views.completeTodo,name='completeTodo'),
    path('todo/<int:todo_pk>/delete',views.deleteTodo,name='deleteTodo'),
    path('currentPage/',views.currentPage,name='currentPage'),
    path('completed/',views.completedTodo,name='completedTodo'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
