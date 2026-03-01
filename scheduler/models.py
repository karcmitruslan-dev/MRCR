from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО преподавателя')

    class Meta:
        ordering = ['name']
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return self.name


class Subject(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название предмета')

    class Meta:
        ordering = ['title']
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название группы')

    class Meta:
        ordering = ['name']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name


class Schedule(models.Model):
    DAY_CHOICES = [
        ('Пн', 'Понедельник'),
        ('Вт', 'Вторник'),
        ('Ср', 'Среда'),
        ('Чт', 'Четверг'),
        ('Пт', 'Пятница'),
        ('Сб', 'Суббота'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='schedules', verbose_name='Группа')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules', verbose_name='Предмет')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules', verbose_name='Преподаватель')
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES, verbose_name='День недели')
    time = models.TimeField(verbose_name='Время занятия')

    class Meta:
        ordering = ['group__name', 'time']
        verbose_name = 'Запись расписания'
        verbose_name_plural = 'Расписание'
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'day_of_week', 'time'],
                name='unique_group_day_time_slot'
            )
        ]

    def __str__(self):
        return f'{self.group} | {self.day_of_week} {self.time:%H:%M} | {self.subject}'
