from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('on/<str:keyword>', views.onLED, name='on-led'),
    path('off/<str:keyword>', views.offLED, name='off-led'),
    
    path('list/<str:keyword>/', views.LedDetail.as_view(), name='led')
]