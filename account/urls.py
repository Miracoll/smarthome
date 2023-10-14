from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('controls/', views.control, name='control'),
    path('configuration/', views.config, name='config'),
    path('add/user/', views.addUser, name='add-user'),
    path('logs/', views.viewLog, name='log'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('on/<str:ref>', views.onLED, name='on-led'),
    path('off/<str:ref>', views.offLED, name='off-led'),
    path('level-zero/<str:ref>', views.levelZero, name='level-zero'),
    path('level-one/<str:ref>', views.levelOne, name='level-one'),
    path('level-two/<str:ref>', views.levelTwo, name='level-two'),
    path('level-three/<str:ref>', views.levelThree, name='level-three'),
    path('level-four/<str:ref>', views.levelFour, name='level-four'),
    
    path('api/list/<str:ref>/', views.LedDetail.as_view(), name='led'),
    path('api/config/', views.ConfigDetail.as_view(), name='api-config')
]