# -*- coding: utf-8 -*-
from django.forms import ModelForm
from demo.models import Film, Hall, Session


class SessionModelForm(ModelForm):
    bootstrap_options = {
        'as_p_use_divs': True,
        'form_layout': 'form-horizontal',
    }

    def save(self, *args, **kwargs):
        preferences = super(SessionModelForm, self).save(
            commit=False,
            *args,
            **kwargs
        )
        preferences.save()
        return preferences

    class Meta:
        model = Session
        fields = '__all__'


class FilmModelForm(ModelForm):
    bootstrap_options = {
        'as_p_use_divs': True,
        'form_layout': 'form-horizontal',
    }

    def save(self, *args, **kwargs):
        preferences = super(FilmModelForm, self).save(
            commit=False,
            *args,
            **kwargs
        )
        preferences.save()
        return preferences

    class Meta:
        model = Film
        fields = '__all__'