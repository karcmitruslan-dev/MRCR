from collections import OrderedDict

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import GroupForm, ScheduleForm, SubjectForm, TeacherForm
from .models import Group, Schedule, Subject, Teacher

DAY_ORDER = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
DAY_TITLES = {
    'Пн': 'Понедельник',
    'Вт': 'Вторник',
    'Ср': 'Среда',
    'Чт': 'Четверг',
    'Пт': 'Пятница',
    'Сб': 'Суббота',
}


def _build_timetable(schedule_qs):
    entries = list(
        schedule_qs.select_related('group', 'subject', 'teacher').order_by('time', 'group__name', 'day_of_week')
    )

    times = sorted({entry.time for entry in entries})
    timetable = OrderedDict()
    for slot in times:
        timetable[slot] = {day: [] for day in DAY_ORDER}

    for entry in entries:
        timetable[entry.time][entry.day_of_week].append(entry)

    return timetable, entries


def schedule_home(request):
    groups = Group.objects.all()
    selected_group_id = request.GET.get('group')
    schedule_qs = Schedule.objects.all()
    selected_group = None

    if selected_group_id:
        try:
            selected_group = groups.get(pk=int(selected_group_id))
            schedule_qs = schedule_qs.filter(group=selected_group)
        except (ValueError, Group.DoesNotExist):
            messages.warning(request, 'Выбрана некорректная группа. Показано всё расписание.')
            selected_group_id = ''

    timetable, entries = _build_timetable(schedule_qs)

    stats = {
        'groups_count': Group.objects.count(),
        'teachers_count': Teacher.objects.count(),
        'subjects_count': Subject.objects.count(),
        'classes_count': Schedule.objects.count(),
    }

    context = {
        'groups': groups,
        'selected_group_id': str(selected_group_id or ''),
        'selected_group': selected_group,
        'day_order': DAY_ORDER,
        'day_titles': DAY_TITLES,
        'timetable': timetable,
        'entries': entries,
        'stats': stats,
    }
    return render(request, 'scheduler/home.html', context)


def schedule_add(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись расписания успешно добавлена.')
            return redirect('scheduler:home')
    else:
        form = ScheduleForm()

    return render(request, 'scheduler/schedule_form.html', {'form': form, 'page_title': 'Добавить занятие'})


def schedule_edit(request, pk):
    instance = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись расписания обновлена.')
            return redirect('scheduler:home')
    else:
        form = ScheduleForm(instance=instance)

    return render(request, 'scheduler/schedule_form.html', {'form': form, 'page_title': 'Редактировать занятие'})


def teacher_list(request):
    teachers = Teacher.objects.annotate(classes_count=Count('schedules'))
    return render(request, 'scheduler/teacher_list.html', {'teachers': teachers})


def teacher_add(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Преподаватель добавлен.')
            return redirect('scheduler:teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'scheduler/simple_form.html', {'form': form, 'page_title': 'Добавить преподавателя'})


def subject_list(request):
    subjects = Subject.objects.annotate(classes_count=Count('schedules'))
    return render(request, 'scheduler/subject_list.html', {'subjects': subjects})


def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Предмет добавлен.')
            return redirect('scheduler:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'scheduler/simple_form.html', {'form': form, 'page_title': 'Добавить предмет'})


def group_list(request):
    groups = Group.objects.annotate(classes_count=Count('schedules'))
    return render(request, 'scheduler/group_list.html', {'groups': groups})


def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Группа добавлена.')
            return redirect('scheduler:group_list')
    else:
        form = GroupForm()
    return render(request, 'scheduler/simple_form.html', {'form': form, 'page_title': 'Добавить группу'})
