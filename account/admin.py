from django.contrib import admin
from .models import User, Control, Config, Test

# Register your models here.

admin.site.register(User)
admin.site.register(Control)
admin.site.register(Config)
admin.site.register(Test)