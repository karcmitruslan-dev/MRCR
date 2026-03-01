from django import forms

from .models import Group, Schedule, Subject, Teacher


class BootstrapMixin:
    """Добавляет Bootstrap-классы ко всем полям формы."""

    def _apply_bootstrap(self):
        for name, field in self.fields.items():
            widget = field.widget
            css_class = widget.attrs.get('class', '')
            if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                widget.attrs['class'] = (css_class + ' form-check-input').strip()
            else:
                widget.attrs['class'] = (css_class + ' form-control').strip()

            if name == 'time':
                widget.attrs['type'] = 'time'


class ScheduleForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['group', 'subject', 'teacher', 'day_of_week', 'time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class TeacherForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class SubjectForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class GroupForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
