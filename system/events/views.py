from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django .contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django .contrib.auth import authenticate,login,logout
from . decorators import unauthenticated_user,allowed_users,admin_only


from .forms import UnitForm,CreateUserForm,BookForm
from .filters import  UnitFilter




# Create your views here.

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')

            group =Group.objects.get(name='student')

            user.groups.add(group)
            messages.success(request, 'Account was successfully created for' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'events/register.html', context)


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
            messages.info(request, 'username OR password is incorrect')

    context = {}
    return render(request, 'events/login.html', context)


def userPage(request):
    context = {}
    return render(request,'events/user.html',context)

def logoutUser(request):
    logout(request)
    return  redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    students = student.objects.all()
    units = unit.objects.all()
    teachers = teacher.objects.all()

    total_teachers= teachers.count()
    total_units = units.count()
    total_students =students.count()

    context = {'units':units,'teachers':teachers,
               'total_units':total_units,
               'total_students':total_students,
               'total_teachers':total_teachers}

    return render(request,'events/dashboard.html',context)

@login_required(login_url='login')
def students(request):

    students= student.objects.all()

    context = {'students':students}

    return render(request,'events/students.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','teacher'])

def teachers(request,pk_test):

    teachers = teacher.objects.get(id=pk_test)

    units = teachers.unit_set.all()
    unit_count = units.count()

    myfilter = UnitFilter(request.GET,queryset=units)
    units = myfilter.qs

    context = {'teachers':teachers,'units':units,'unit_count':unit_count,'myfilter':myfilter}

    return render(request,'events/teacher.html',context)

@login_required(login_url='login')
def units(request):

    units = unit.objects.all()

    context={'units':units}

    return render(request,'events/units.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','teacher'])

def createUnit(request,pk):
    UnitFormSet = inlineformset_factory(teacher,unit, fields=('unitcode','unitname'),extra = 8)
    teachers = teacher.objects.get(id=pk)
    formset = UnitFormSet(queryset = unit.objects.none(),instance=teachers)
    if request.method=='POST':
        formset = UnitFormSet(request.POST,instance=teachers)
        if formset.is_valid():
            formset.save()
            return  redirect('/')

    context = {'formset':formset}

    return render(request,'events/unit_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','teacher'])

def updateUnit(request,pk):

    units = unit.objects.get(id=pk)
    formset = UnitForm(instance=units)

    if request.method=='POST':
        formset= UnitForm(request.POST,instance=units)
        if formset.is_valid():
            formset.save()
            return  redirect('/')

    context = {'formset': formset}

    return render(request, 'events/unit_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def deleteUnit(request,pk):
    units = unit.objects.get(id=pk)

    if request.method == "POST":
        units.delete()
        return redirect('/')

    context = {'item':units}
    return render(request,'events/delete.html',context)

#notes upload page

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','teacher'])
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'events/upload_book.html', {
        'form': form
    })

def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


def book_list(request):
    books = Book.objects.all()
    return render(request, 'events/book_list.html', {
        'books': books
    })

#chatbot views
def chat(request):
    return render(request, 'events/home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'events/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/' + room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + room + '/?username=' + username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})