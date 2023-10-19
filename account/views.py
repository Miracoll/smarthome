from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from .models import Control, User, Config, History
from .serializers import LEDSerializer, ConfigSerializer
from .forms import ControlForm, ConfigForm
from .functions import sendMessage, extract_lat_lng, addHistory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from time import sleep
import paho.mqtt.client as mqtt 
from random import randrange, uniform

# Create your views here.

# def home(request):
#     led = LED.objects.get(keyword='led1')
#     context = {'led':led}
#     return render(request, 'account/index.html', context)

# def createDevice(request):
#     context = {}
#     return render(request, 'account/create-device.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['visitor','admin'])
def home(request):
    control = Control.objects.all()
    context = {'control':control}
    return render(request, 'account/index.html', context)

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Unauthorised access')
            return redirect('login')
    return render(request, 'account/login.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['visitor','admin'])
def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['visitor','admin'])
def control(request):
    user = request.user
    control = Control.objects.all()
    form = ControlForm()
    if request.method == 'POST':
        form = ControlForm(request.POST, request.FILES)
        password = request.POST.get('pass')
        if user.check_password(password):
            if form.is_valid():
                con = form.save(commit=False)
                con.name = request.POST.get('name').upper()
                con.keyword = request.POST.get('keyword')
                con.user = request.user
                form.save()
                messages.success(request, 'Added')
                return redirect('control')
        else:
            threatCounter = int(user.threat_counter)
            if threatCounter >= 2:
                user.is_active = False
                user.reason = 'Max. password attempt in control'
                user.save()
            else:
                print(user.threat_counter)
                threatCounter += 1
                user.threat_counter = threatCounter
                user.save()
            messages.error(request, 'Unauthorized access')
            return redirect('control')
    context = {
        'control':control,
        'form':form,
    }
    return render(request, 'account/control.html', context)

def onLED(request, ref):
    # op = Control.objects.get(ref=ref)
    # config = Config.objects.get(id=1)
    # mqttBroker ="mqtt.eclipseprojects.io"
    # client = mqtt.Client(f'{op.ref}')
    # client.connect(mqttBroker) 
    # status = 'ON'
    # client.publish(f'{op.name}', status)
    # print(f"Just published  {status}  to topic {op.name}")
    # sleep(1)
    # if op.status:
    #     messages.info(request, f'{op.name} is already on')
    #     return redirect('control')
    # op.status = True
    # op.save()
    
    op = Control.objects.get(ref=ref)
    config = Config.objects.get(id=1)
    if not op.connection_status:
        messages.error(request, 'No connection')
        return redirect('control')
    if op.status:
        messages.info(request, f'{op.name} is already on')
        return redirect('control')
    op.status = True
    op.save()
    sendMessage(f'{request.user} just turned on {op.name}')
    addHistory(request, f'Turned on {op.name}')
    messages.success(request, 'ON')
    return redirect('control')
    
def offLED(request, ref):

    # op = Control.objects.get(ref=ref)
    # config = Config.objects.get(id=1)
    # mqttBroker ="mqtt.eclipseprojects.io"
    # client = mqtt.Client(f'{op.ref}')
    # client.connect(mqttBroker) 
    # status = 'OFF'
    # client.publish(f'{op.name}', status)
    # print(f"Just published  {status}  to topic {op.name}")
    # sleep(1)
    # if not op.status:
    #     messages.info(request, f'{op.name} is already off')
    #     return redirect('control')
    # op.status = False
    # op.save()
    
    op = Control.objects.get(ref=ref)
    config = Config.objects.get(id=1)
    if not op.connection_status:
        messages.error(request, 'No connection')
        return redirect('control')
    if not op.status:
        messages.info(request, f'{op.name} is already off')
        return redirect('control')
    op.status = False
    op.save()
    sendMessage(f'{request.user} just turned off {op.name}')
    addHistory(request, f'Turned off {op.name}')
    messages.success(request, 'OFF')
    return redirect('control')

def refreshControl(request):
    counter = 0
    config = Config.objects.get(id=1)
    config.acknowledge_request = False
    while not config.acknowledge_response:
        if counter >= 50:
            config.connection_status = False
            config.save()
            messages.error(request, 'No connection')
            return redirect('control')
        sleep(0.5)
        counter += 1
    config.connection_status = True
    config.save()
    messages.success(request, 'Connected')
    return redirect('control')

def levelZero(request, ref):
    op = Control.objects.get(ref=ref)
    if not op.status and op.level == 0:
        messages.info(request, f'{op.name} is already in level zero(off)')
        return redirect('control')
    op.status = False
    op.level = 0
    op.save()
    sendMessage(f'{request.user} just turned off {op.name} to level zero(off)')
    addHistory(request, f'Turned off {op.name} to level 0(off)')
    messages.success(request, 'Triggered')
    return redirect('control')

def levelOne(request, ref):
    op = Control.objects.get(ref=ref)
    if op.status and op.level == 1:
        messages.info(request, f'{op.name} is already in level 1(on)')
        return redirect('control')
    op.status = True
    op.level = 1
    op.save()
    sendMessage(f'{request.user} just turned on {op.name} to level 1(on)')
    addHistory(request, f'Turned on {op.name} to level 1')
    messages.success(request, 'Triggered')
    return redirect('control')

def levelTwo(request, ref):
    op = Control.objects.get(ref=ref)
    if op.status and op.level == 2:
        messages.info(request, f'{op.name} is already in level 2(on)')
        return redirect('control')
    op.status = True
    op.level = 2
    op.save()
    sendMessage(f'{request.user} just turned on {op.name} to level 2(on)')
    addHistory(request, f'Turned on {op.name} to level 2')
    messages.success(request, 'Triggered')
    return redirect('control')

def levelThree(request, ref):
    op = Control.objects.get(ref=ref)
    if op.status and op.level == 3:
        messages.info(request, f'{op.name} is already in level 3(on)')
        return redirect('control')
    op.status = True
    op.level = 3
    op.save()
    sendMessage(f'{request.user} just turned on {op.name} to level 3(on)')
    addHistory(request, f'Turned on {op.name} to level 3')
    messages.success(request, 'Triggered')
    return redirect('control')

def levelFour(request, ref):
    op = Control.objects.get(ref=ref)
    if op.status and op.level == 4:
        messages.info(request, f'{op.name} is already in level 4(on)')
        return redirect('control')
    op.status = True
    op.level = 4
    op.save()
    sendMessage(f'{request.user} just turned on {op.name} to level 4(on)')
    addHistory(request, f'Turned on {op.name} to level 4')
    messages.success(request, 'Triggered')
    return redirect('control')

@login_required(login_url='login')
@allowed_users(allowed_roles=['visitor','admin'])
def config(request):
    user = request.user
    config = Config.objects.get(id=1)
    form = ConfigForm(instance=config)
    if request.method == 'POST':
        form = ConfigForm(request.POST, instance=config)
        password = request.POST.get('pass')
        if user.check_password(password):
            if form.is_valid():
                form.save()
                messages.success(request, 'updated')
                return redirect('config')
        else:
            threatCounter = int(user.threat_counter)
            if threatCounter >= 2:
                user.is_active = False
                user.reason = 'Max. password attempt in configuration'
                user.save()
            else:
                print(user.threat_counter)
                threatCounter += 1
                user.threat_counter = threatCounter
                user.save()
            messages.error(request, 'Unauthorized access')
            return redirect('config')
    context = {
        'form':form,
    }
    return render(request, 'account/configuration.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['visitor','admin'])
def addUser(request):
    user = request.user
    if request.method == 'POST':
        last = request.POST.get('last_name')
        first = request.POST.get('first_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('pass')
        if user.check_password(confirm):
            person = User.objects.create_user(username,email,password)
            person.is_active = True
            person.last_name = last
            person.first_name = first
            person.email = email
            role = 'visitor'
            person.save()

            if not Group.objects.filter(name=role).exists():
                Group.objects.create(name=role)
                getgroup = Group.objects.get(name=role)
                getgroup.user_set.add(person.id)

            messages.success(request, 'Created')
            return redirect('add-user')
        else:
            threatCounter = int(user.threat_counter)
            if threatCounter >= 2:
                user.is_active = False
                user.reason = 'Max. password attempt when adding user'
                user.save()
            else:
                print(user.threat_counter)
                threatCounter += 1
                user.threat_counter = threatCounter
                user.save()
            messages.error(request, 'Unauthorized access')
            return redirect('config')
    context = {}
    return render(request, 'account/add_user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['visitor','admin'])
def viewLog(request):
    history = History.objects.all()
    context = {'history':history}
    return render(request, 'account/logs.html', context)

class LedDetail(APIView):
    
    def get(self, request, ref):
        try:
            led = Control.objects.get(ref=ref)
        except Control.DoesNotExist:
            return Response({'error':'not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LEDSerializer(led)
        return Response(serializer.data)

class ControlList(APIView):
    def get(self, request):
        try:
            control = Control.objects.all()
        except Control.DoesNotExist:
            return Response({'error':'not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LEDSerializer(control, many=True)
        return Response(serializer.data)
    
class ConfigDetail(APIView):
    def get(self, request, ref):
        try:
            config = Config.objects.get(id=ref)
        except Config.DoesNotExist:
            return Response({'error':'not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConfigSerializer(config)
        return Response(serializer.data)
    
    def put(self, request, ref):
        config = Config.objects.get(id=ref)
        serializer = ConfigSerializer(config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ConfigResponse(APIView):
    def put(self, request, ref):
        # try:
        config = Config.objects.get(id=ref)
        config.connection_status = True
        config.save()
        # except Config.DoesNotExist:
        #     return Response({'error':'not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConfigSerializer(config)
        return Response(serializer.data)