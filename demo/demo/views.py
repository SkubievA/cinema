# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from demo.models import Film, Hall, Session
from demo.forms import SessionModelForm
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response


def add_session(request):
    session_edit_form = SessionModelForm(instance=Session.objects.get(id=1))
    if request.method == "POST":
        form = SessionModelForm(data=request.POST)
        if form.is_valid():
            form = form.save()
            if request.is_ajax():
                return HttpResponse('true')
            messages.success(request, 'Preferences saved')
        elif request.is_ajax():
            return HttpResponse('false')
    else:
        form = None
    template_name = 'demo/session.html'
    return render_to_response(template_name,
                              RequestContext(request, {
                                  'formadd': form,
                                  'formedit': session_edit_form,
                                  "id_session": 1,
                                  "list_session": Session.objects.all(),
                              }))


def edit_session(request, id):
    session_add_form = SessionModelForm()
    try:
        preferences = Session.objects.get(
            id=id
        )
    except Session.DoesNotExist:
        preferences = None

    if request.method == "POST":
        form = SessionModelForm(data=request.POST,
                                instance=preferences)
        if form.is_valid():
            preferences = form.save()
            if request.is_ajax():
                return HttpResponse('true')
            messages.success(request, 'Preferences saved')
        elif request.is_ajax():
            return HttpResponse('false')
    else:
        form = SessionModelForm(
            id=id,
            instance=preferences
        )
    template_name = 'demo/session.html'
    return render_to_response(template_name,
                              RequestContext(request, {
                                  'formadd': session_add_form,
                                  'formedit': form,
                                  "id_session": id,
                                  "list_session": Session.objects.all(),
                              }))


class HomePageView(TemplateView):
    template_name = 'demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update({
            "language": "fffsd",
            })
        return context


class ScheduleView(TemplateView):
    template_name = 'demo/schedule.html'


class SessionView(TemplateView):
    template_name = 'demo/session.html'
    session_add_form = SessionModelForm()
    session_edit_form = SessionModelForm(instance=Session.objects.get(id=1))
    # session_form = inlineformset_factory(Hall, Session)
    # session = Session.objects.get(pk=1)
    # session_form = session_form(instance=session)

    def get_context_data(self, **kwargs):
        context = super(SessionView, self).get_context_data(**kwargs)

        context.update({
            "list_session": Session.objects.all(),
            "formadd": self.session_add_form,
            "formedit": self.session_edit_form,
            "id_session": 1,
            })
        return context
