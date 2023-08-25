from django.contrib import admin
from . models import InterimFields, Employee
from import_export.admin import ImportExportModelAdmin


class InterimAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'employee_id', 'reporting_manager', 'num_of_days', 'start_date', 'end_date', 'status')
    list_editable = ['status']
admin.site.register(InterimFields, InterimAdmin)

class EmployeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('Employee', 'FirstNameLastName', 'WorkEmail')
admin.site.register(Employee, EmployeeAdmin )