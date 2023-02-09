from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import CreateUserForm, CreateUserFormTeacher
from .decorators import unauthenticated_user
# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            role = form.cleaned_data.get('role')

            group = Group.objects.get(name=role)
            user.groups.add(group)

            if role == 'student':
                Student.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
            elif role == 'parent':
                Parent.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )

            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def registerPageTeacher(request):
    form = CreateUserFormTeacher()

    if request.method == "POST":
        form = CreateUserFormTeacher(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name='teacher')
            user.groups.add(group)

            Teacher.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect.')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect("login")

@login_required(login_url='login')
def home(request):
    is_teacher = request.user.groups.filter(name ='teacher').exists()
    is_student = request.user.groups.filter(name ='student').exists()
    is_parent = request.user.groups.filter(name ='parent').exists()
    context = {'is_teacher': is_teacher, 'is_student': is_student, 'is_parent':is_parent}
    return render(request, 'accounts/home.html', context)
