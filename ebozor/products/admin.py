from django.contrib import admin

# Register your models here.
from .models import User,Contract,Fakultet,Test

admin.site.register(User)
admin.site.register(Test)
admin.site.register(Fakultet)
admin.site.register(Contract)