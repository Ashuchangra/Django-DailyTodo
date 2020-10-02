from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout,authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'todo/home.html')
@login_required
def createTodo(request):
    if request.method=='GET':
        return render(request,'todo/createTodo.html', {'form':TodoForm})
    else:
        try:
            form=TodoForm(request.POST)
            newForm= form.save(commit=False)
            newForm.user=request.user
            newForm.save()
            return redirect('currentPage')
        except ValueError:
            return render(request,'todo/createTodo.html', {'form':TodoForm,'error':'Invalid data entered, please try again'})




def loginuser(request):
    if request.method=='GET':
        return render(request, 'todo/login.html',{'loginform':AuthenticationForm})
    else:
        user=authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request,user)
            return redirect('currentPage')
        else:
            return render(request,'todo/login.html',{'loginform':AuthenticationForm,'error':'Invalid Credentials'})

def signupuser(request):
    if request.method=='GET':
        return render(request,'todo/signup.html',{'form':UserCreationForm})
    else:
        if request.POST['password1']== request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentPage')
            except IntegrityError:
                return render(request,'todo/signup.html',{'form':UserCreationForm,'error':'Username already taken, please choose new username'})
        else:
            return render(request,'todo/signup.html',{'form':UserCreationForm,'error':'Password Mismatch!!!'})

@login_required
def logoutUser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

@login_required
def currentPage(request):
    todos=Todo.objects.filter(user=request.user,dateCompletion__isnull=True)
    return render(request,'todo/currentPage.html',{'todos':todos})

@login_required
def viewTodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method=='GET':
        form=TodoForm(instance=todo)
        return render(request,'todo/viewtodo.html',{'todo':todo,'form':form})
    else:
        form=TodoForm(request.POST,instance=todo)
        form.save()
        return redirect('currentPage')

@login_required
def completeTodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method=='POST':
        todo.dateCompletion=timezone.now()
        todo.save()
        return redirect('currentPage')

@login_required
def deleteTodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method=='POST':
        todo.delete()
        return redirect('currentPage')
@login_required 
def completedTodo(request):
    todos=Todo.objects.filter(user=request.user,dateCompletion__isnull=False)
    return render(request,'todo/completedTodo.html',{'todos':todos})
