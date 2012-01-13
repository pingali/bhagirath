from django.contrib import admin
from models import Task,Subtask,StaticMicrotask,Microtask,UserProfile,UserHistory

admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(StaticMicrotask)
admin.site.register(Microtask)
admin.site.register(UserProfile)
admin.site.register(UserHistory)