from django.contrib import admin

# Register your models here.
from .models import User,Contract,Fakultet,Test


# common/admin.py
admin.site.register(User)
admin.site.register(Test)
admin.site.register(Fakultet)
# admin.site.register(Contract)
 # Replace 'your_column_name' with the actual column name

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = Contract.DisplayFields
    search_fields = Contract.SearchableFields