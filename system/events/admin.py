from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(teacher)
admin.site.register(student)
admin.site.register(unit)
admin.site.register(Room)
admin.site.register(Message)