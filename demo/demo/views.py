# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from demo.models import Film, Hall, Session
from demo.forms import SessionModelForm, FilmModelForm
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.models import inlineformset_factory


def add_session(request):
    session_edit_form = SessionModelForm(instance=Session.objects.get(id=1))
    if request.method == "POST":
        form = SessionModelForm(data=request.POST)
        if form.is_valid():
            form = form.save()
            if request.is_ajax():
                return HttpResponse('true')
            messages.success(request, 'Новый сеанс добавлен.')
        elif request.is_ajax():
            return HttpResponse('false')
    else:
        form = None
    template_name = 'demo/session.html'
    return render_to_response(template_name,
                              RequestContext(request, {
                                  'formadd': form,
                                  'formedit': session_edit_form,
                                  "list_session": Session.objects.all(),
                              }))


def add_film(request):
    film_edit_form = FilmModelForm(instance=Film.objects.get(id=1))
    if request.method == "POST":
        form = FilmModelForm(data=request.POST)
        if form.is_valid():
            form = form.save()
            if request.is_ajax():
                return HttpResponse('true')
            messages.success(request, 'Новый фильм добавлен.')
        elif request.is_ajax():
            return HttpResponse('false')
    else:
        form = None
    template_name = 'demo/film.html'
    return render_to_response(template_name,
                              RequestContext(request, {
                                  'formadd': FilmModelForm(),
                                  'formedit': film_edit_form,
                                  "list_film": Film.objects.all(),
                              }))


def edit_film(request, id):
    try:
        preferences = Film.objects.get(
            id=id
        )
    except Film.DoesNotExist:
        preferences = None

    if request.method == "POST":
        form = FilmModelForm(data=request.POST,
                             instance=preferences)
        if form.is_valid():
            preferences = form.save()
            if request.is_ajax():
                return HttpResponse('true')
            messages.success(request, 'Данные о фильме обновлены.')
        elif request.is_ajax():
            return HttpResponse('false')
    else:
        form = FilmModelForm(
            id=id,
            instance=preferences
        )
    template_name = 'demo/films.html'
    return render_to_response(template_name,
                              RequestContext(request, {
                                  'formadd': FilmModelForm(),
                                  'formedit': form,
                                  "id_session": id,
                                  "select_film": 3,
                                  "list_film": Film.objects.all(),
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
            messages.success(request, 'Данные о сеансе обновлены.')
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
                                  "id_film": id,
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

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        id = request.POST.get('sel1')[0:request.POST.get('sel1').find('/')]
        session_edit_form = SessionModelForm(instance=Session.objects.get(id=id))
        context['formadd'] = self.session_add_form
        context['formedit'] = session_edit_form
        context['select_session'] = id
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SessionView, self).get_context_data(**kwargs)

        context.update({
            "list_session": Session.objects.all(),
            "formadd": self.session_add_form,
            "formedit": self.session_edit_form,
            })
        return context


class HallView(TemplateView):
    template_name = 'demo/hall.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        number = request.POST.get('hall')
        hall = Hall.objects.get(number=number)
        context['select_number'] = number

        x = 1
        y = 1
        result_html = ''
        while x <= hall.count_series:
            result_html += '<p>' + str(x) + ' |'
            while y <= hall.count_place:
                result_html += '    ' + str(y)
                y += 1
            result_html += '</p>'
            x += 1
            y = 1

        context['hall'] = result_html
        context['title_hall'] = 'Визуальное размещение мест:'
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HallView, self).get_context_data(**kwargs)

        context.update({
            "list_hall": Hall.objects.all(),
            "id_session": 1,
            })
        return context


class FilmsView(TemplateView):
    template_name = 'demo/film.html'
    film_add_form = FilmModelForm()

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        name = request.POST.get('film')
        film = Film.objects.get(film=name)
        context['formadd'] = self.film_add_form
        context['formedit'] = FilmModelForm(instance=film)
        context['select_film'] = name
        context['id_film'] = int(film.id),
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(FilmsView, self).get_context_data(**kwargs)

        context.update({
            "formadd": self.film_add_form,
            "list_film": Film.objects.all(),
            })
        return context
