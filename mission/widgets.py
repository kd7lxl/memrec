from django import forms


class TimeInput(forms.TimeInput):
    format = '%H%M'

    def __init__(self, attrs=None, format=None):
        super(TimeInput, self).__init__(attrs, format=self.format)
