from django.shortcuts import render, redirect
from .forms import MessageForm
from .models import Message, Block
from django.contrib import messages
from django.contrib.auth.models import User
from student.models import Student
from student.models import Profile
from .filters import UserFilter
import json
from django.http import HttpResponse

# Create your views here.


def send(request):
    if request.method == 'POST':
        receiver_id = request.POST['receiver_id']
        receiver_list = receiver_id.split(',')
        sender = request.user

        for instance in receiver_list:
            message_form = MessageForm(request.POST, request.FILES)
            if message_form.is_valid():
                print(instance)
                form = message_form.save(commit=False)
                form.receiver = User.objects.get(id=instance)
                form.sender = sender
                form.save()
        context = {'form': message_form}
        return render(request, 'communication/send.html', context)

    else:
        form = MessageForm()
        receiver = User.objects.raw('select id,username,first_name,last_name from auth_user')
        context = {'form': form, 'receiver': receiver}
        return render(request, 'communication/send.html', context)
    return render(request, 'communication/send.html', {'form': message_form})


def receive(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(first_name__icontains=q)
        results = []
        for i in users:
            users_json = {}
            users_json['label'] = i.first_name + " " + i.last_name
            users_json['value'] = i.first_name + " " + i.last_name
            users_json['id'] = i.id
            results.append(users_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def read(request):
    receiver = request.user.id
    message = Message.objects.raw("Select * from communication_message where receiver_id = %s group by sender_id", [receiver])
    return render(request, 'communication/receive.html', {'form': message})


def read_view(request, pk):
    message = Message.objects.raw("Select * from communication_message where sender_id = %s order by date desc",
                                  [pk])
    return render(request, 'communication/read_view.html', {'form': message, 'sender': pk})


def block(request, pk):
    sender = User.objects.get(id=pk)
    Block.objects.create(receiver=request.user, sender=sender)
    return redirect('communication:read')


def unblock(request, pk):
    receiver = request.user.id
    Block.objects.filter(sender=pk, receiver=receiver).delete()
    return redirect('communication:read')