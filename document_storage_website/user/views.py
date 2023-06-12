from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, add_pass_form, delete_pass_form, edit_pass_form
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from user.models import user, pass_data
from django.db.models import Q
from ast import literal_eval
from datetime import datetime
  
  
def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            u = user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            u.save()
            messages.success(request, 'Successfully Registered.')
            return _login(request, form.cleaned_data['username'], form.cleaned_data['password1'])
    return render(request, 'user/register.html', {'form': form})
  
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        return _login(request, username, password)
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form})

def _login(request, username, password):
    user = authenticate(request, username = username, password = password)
    if user is not None:
        login(request, user)
        return redirect('display')
    else:
        messages.error(request, f'Username or Password is incorrect.')

@login_required(login_url="login")
def display(request):
    u = user.objects.get(username=request.user.username)
    data = pass_data.objects.all().filter(user_id=u)
    return render(request, 'user/display.html', {'data':data})

@login_required(login_url="login")
def add_pass(request):
    form = add_pass_form(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            u = user.objects.get(username=request.user.username)
            p = pass_data(user_id=u, name=form.cleaned_data['name'], username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            p.save()
            messages.success(request, 'Successfully Added.')
            return redirect('display')
    return render(request, 'user/add_pass.html', {'form':form})

@login_required(login_url="login")
def delete_pass(request):
    form = delete_pass_form(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print(11111111111111)
            print(form.cleaned_data['names'])
            names = literal_eval(form.cleaned_data['names'])
            names = [name[:-len('_check')] for name in names]
            u = user.objects.get(username=request.user.username)
            c1 = Q(user_id=u)
            c2 = Q(name__in=names)
            pass_data.objects.filter(c1 & c2).delete()
            messages.success(request, 'Successfully Removed.')
    return redirect('display')

@login_required(login_url="login")
def edit_pass(request, id):
    if request.method == "POST":
        form = edit_pass_form(request.POST)
        if form.is_valid():
            u = user.objects.get(username=request.user.username)
            c1 = Q(user_id=u)
            c2 = Q(id=id)
            p = pass_data.objects.get(c1 & c2)
            p.name = form.cleaned_data['name']
            p.username = form.cleaned_data['username']
            p.password = form.cleaned_data['password']
            p.last_modified_date = datetime.now()
            p.save()
            messages.success(request, 'Successfully Edited.')
            return redirect('display')
    if request.method == "GET":
        u = user.objects.get(username=request.user.username)
        c1 = Q(user_id=u)
        c2 = Q(id=id)
        p = pass_data.objects.get(c1 & c2)
        initial={'name':p.name,'username':p.username,'password':p.password}
        return render(request, 'user/edit_pass.html', {'initial':initial, 'id':id})
    else:
        return redirect('display')
 