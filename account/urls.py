from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('refresh/', views.refreshControl, name='refresh'),
    path('level-zero/<str:ref>', views.levelZero, name='level-zero'),
    path('level-one/<str:ref>', views.levelOne, name='level-one'),
    path('level-two/<str:ref>', views.levelTwo, name='level-two'),
    path('level-three/<str:ref>', views.levelThree, name='level-three'),
    path('level-four/<str:ref>', views.levelFour, name='level-four'),
    
    path('api/list/', views.ControlList.as_view(), name='api-device'),
    path('api/device/<str:ref>/', views.LedDetail.as_view(), name='led'),
    path('api/config/<str:ref>', views.ConfigDetail.as_view(), name='api-config'),
    path('api/config/response/<int:ref>', views.ConfigResponse.as_view(), name='api-config-response'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='account/reset_password_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='account/passsword_reset_complete.html'), name='password_reset_complete'),
]