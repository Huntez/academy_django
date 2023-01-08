from django.contrib import admin
from Hospital.models import *

# Register your models here.

admin.site.register(Department)
admin.site.register(Disease)
admin.site.register(Examination)
admin.site.register(Doctor)
admin.site.register(Ward)
