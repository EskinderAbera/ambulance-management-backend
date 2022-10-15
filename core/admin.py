from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Hospital)
admin.site.register(Driver)
admin.site.register(Role)
admin.site.register(Profile)
admin.site.register(SenderMessage)