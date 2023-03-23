from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Upload)
admin.site.register(UserDepartment)