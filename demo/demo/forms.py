# -*- coding: utf-8 -*-
from demo.models import Session
from django.forms import ModelForm


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