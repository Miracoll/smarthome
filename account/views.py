from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LED
from .serializers import LEDSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def home(request):
    if request.method == 'POST':
        pass
    context = {}
    return render(request, 'account/index.html', context)

class LedDetail(APIView):
    
    def get(self, request, keyword):
        try:
            led = LED.objects.get(keyword=keyword)
        except LED.DoesNotExist:
            return Response({'error':'not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LEDSerializer(led)
        return Response(serializer.data)

def onLED(request, keyword):
    op = LED.objects.get(keyword=keyword)
    op.status = True
    op.save()
    messages.success(request, 'ON')
    return redirect('home')
    
def offLED(request, keyword):
    op = LED.objects.get(keyword=keyword)
    op.status = False
    op.save()
    messages.success(request, 'OFF')
    return redirect('home')

# def createDevice(request):
#     context = {}
#     return render(request, 'account/create-device.html', context)