from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Agents)
admin.site.register(Contact)
admin.site.register(Property)