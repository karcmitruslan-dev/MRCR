from django.contrib import admin

from .models import Group, Schedule, Subject, Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'subject', 'teacher', 'day_of_week', 'time')
    list_filter = ('group', 'day_of_week', 'teacher')
    search_fields = ('group__name', 'subject__title', 'teacher__name')
    ordering = ('group__name', 'day_of_week', 'time')
