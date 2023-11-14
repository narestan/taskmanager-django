from django.contrib import admin

from .models import User, Task, Agent, UserProfile, Category, FollowUp


class TaskAdmin(admin.ModelAdmin):
    # fields = (
    #     'task_name',
    #
    # )

    list_display = ['task_name', 'info']
    list_display_links = ['task_name']
    list_filter = ['category']
    search_fields = ['task_name']


admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Task, TaskAdmin)
admin.site.register(Agent)
admin.site.register(FollowUp)
