from django.contrib import admin



from .models import StaffProfile, Task, UserProfile

admin.site.register(StaffProfile)
admin.site.register(Task)
admin.site.register(UserProfile)
