from django.contrib import admin

# Register your models here.
from .models import User,Contract,Fakultet,Test
# class ContractAdmin(admin.ModelAdmin):
#     list_filter = ('id','phone','passport')
admin.site.register(User)
admin.site.register(Test)
admin.site.register(Fakultet)

 # Replace 'your_column_name' with the actual column name

admin.site.register(Contract)