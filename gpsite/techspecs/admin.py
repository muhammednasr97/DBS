from django.contrib import admin
from .models import Equipment, Technical_Report, Technical_Specs, General_Specs


admin.site.register(Technical_Specs)
admin.site.register(General_Specs)
admin.site.register(Equipment)
admin.site.register(Technical_Report)


