from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Technical_Report, Technical_Specs, General_Specs, Technical_Report_Copy


admin.site.register(Technical_Specs, SimpleHistoryAdmin)
admin.site.register(General_Specs, SimpleHistoryAdmin)
admin.site.register(Technical_Report, SimpleHistoryAdmin)
admin.site.register(Technical_Report_Copy, SimpleHistoryAdmin)




