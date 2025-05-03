from django.contrib import admin
from .models import Us, DailyMessage, SelectedDailyMessage

admin.site.register(Us)
admin.site.register(DailyMessage)
admin.site.register(SelectedDailyMessage)