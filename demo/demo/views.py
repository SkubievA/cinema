# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from demo.models import Film, Hall, Session, Place
from demo.forms import SessionModelForm, FilmModelForm
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime, timedelta, date


def add_session(request):
    sess = Session.objects.order_by('-id')[0]
    session_edit_form = SessionModelForm(instance=Session.objects.get(id=sess.id))
    if request.method == "POST":
        form = SessionModelForm(data=request.POST)
        if form.is_valid():
            form = form.save()
            if request.is_ajax():
                return HttpResponse('true')
            hall = Hall.objects.get(number=request.POST.get('hall'))
            x = 1
            y = 1
            while x <= hall.count_series:
                while y <= hall.count_place:
                    place = Place(status=0,
                                  session_id=sess.id+1,
                                  number_place=y,
                                  number_series=x,
                                  price=100
                    )
                    y += 1
                    place.save()
                y = 1
                x += 1
            messages.success(request, 'Новый сеанс добавлен.')
        elif request.is_ajax():
            return HttpResponse('false')
    else:
        form = None
    template_name = 'demo/session.html'
    return render_to_response(template_name,
                              RequestContext(request, {
                                  'formadd': SessionModelForm(),
                                  'formedit': session_edit_form,
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


class SessionView(TemplateView):
    sess = Session.objects.order_by('-id')[0]
    template_name = 'demo/session.html'
    session_add_form = SessionModelForm()
    session_edit_form = SessionModelForm(instance=Session.objects.get(id=sess.id))

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


class HomePageView(TemplateView):
    template_name = 'demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update({
            "language": "fffsd",
            })
        return context


def view_schedule(request, id):
    try:
        preferences = Session.objects.get(
            id=id
        )
    except Session.DoesNotExist:
        preferences = None

    result_html = '<table class="table table-hover" width="100%">'
    result_html += '<tr><td><b>Фильм:</b> %s</td></tr>' % preferences.film.film
    result_html += '<tr><td><b>Дата и время сеанса:</b> %s</td></tr>' % preferences.date_time
    result_html += '<tr><td><b>Продолжительность:</b> %s</td></tr>' % preferences.time_session
    result_html += '</table>'
    result_html += '<h3>Состояние мест</h3>'
    result_html += '<br><table><tr><td bgcolor="#D3D3D3">100</td><td> - место забронировано</td></tr></table><br>'
    result_html += '<table class="table table-hover" width="100%">'
    hall = Hall.objects.get(id=preferences.hall_id)
    x = 1
    y = 0
    result_html += '<tr><td bgcolor="#E6E6FA"></td>'
    while x <= hall.count_place:
        result_html += '<td bgcolor="#E6E6FA">%s</td>' % x
        x += 1
    result_html += '</tr>'
    x = 1
    result_html += '</tr>'
    while x <= hall.count_series:
        result_html += '<tr>'
        while y <= hall.count_place:
            if y == 0:
                result_html += '<td bgcolor="#E6E6FA">%s</td>' % x
                y += 1
                continue
            place = Place.objects.get(number_series=x, number_place=y, session_id=id)
            place_list = request.GET.getlist('place')
            url = ''
            if place_list:
                for i in place_list:
                    url += '&place=%s' % i
                if str(place.id) in place_list:
                    result_html += '<td bgcolor="#FF0909">%s</td>' % place.price
                    y += 1
                    continue
            if place.status == 0:
                result_html += '<td><a href="?place=%s%s">%s</a></td>' % (place.id, url, place.price)
            else:
                result_html += '<td bgcolor="#D3D3D3">%s</td>' % place.price
            y += 1
        result_html += '</tr>'
        y = 0
        x += 1
    result_html += '</table>'
    result_html += '<a href="/place_handler">Забронировать</a>'
    template_name = 'demo/schedule.html'
    return render_to_response(template_name,
                              RequestContext(request, {
                                  'html': result_html,
                                  }))


class ScheduleView(TemplateView):
    template_name = 'demo/schedule.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.GET.get('day'):
            tmp = request.GET.get('day')
            DATE = date(int(tmp[0:4]), int(tmp[5:7]), int(tmp[8:10]))
        else:
            DATE = datetime.now()

        delta = timedelta(days=1)
        result_html = '<table class="table table-hover"><tr><th>Выберите день:</th></tr>'
        y = 0
        now = datetime.now()
        while y < 10:
            i = now.weekday()
            k = ""
            if i == 0:
                k = "Понедельник"
            if i == 1:
                k = "Вторник"
            if i == 2:
                k = "Среда"
            if i == 3:
                k = "Четверг"
            if i == 4:
                k = "Пятница"
            if i == 5:
                k = "Суббота"
            if i == 6:
                k = "Воскресенье"
            result_html += '<tr><td><a href = "?day=%s">%s, %s</a></td></tr>' % (datetime.strftime(now, "%Y-%m-%d"), now.day, k)
            now += delta
            y += 1

        result_html += '<table class="table table-hover" width="100%">'
        time_start = 10

        result_html += '<tr><th>Время:</th>'
        while time_start < 24:
            result_html += '<th>' + str(time_start) + ' <sup>00</sup></th>'
            time_start += 1
        result_html += '</tr>'

        film = Film.objects.all()
        for f in film:
            session = Session.objects.filter(film=f, status=0)
            result_html += '<tr><td>%s</td></tr><tr>' % f.film
            hall = []
            for s in session:
                hall.append(int(s.hall.number))
            l2 = []
            for i in hall:
                if i not in l2:
                    l2.append(i)
            result_html += '</tr>'
            for i in l2:
                session = Session.objects.filter(film=f, status=0, hall__number=i)
                result_html += '<tr><td>Зал № %s</td>' % i
                # СЕАНС В ВЫБРАННЫЙ ДЕНЬ РИСУЕМ ЕГО В РАСПИСАНИИ
                time_start = 10
                while time_start < 24:
                    for s2 in session:
                        if datetime.strftime(s2.date_time, "%Y.%m.%d") == datetime.strftime(DATE, "%Y.%m.%d"):
                            if time_start == int(datetime.strftime(s2.date_time, "%H")):
                                result_html += '<td bgcolor="#E6E6FA"><a href="/schedule/view/%s">%s</a></td>' % \
                                               (s2.id, datetime.strftime(s2.date_time, "%H:%M"))
                                continue
                    result_html += '<td></td>'
                    time_start += 1
                result_html += '</tr>'
            result_html += '<tr><th>Время:</th>'
            time_start = 10
            while time_start < 24:
                result_html += '<th>' + str(time_start) + ' <sup>00</sup></th>'
                time_start += 1
            result_html += '</tr>'

        result_html += '</table>'
        context["html"] = result_html
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)

        context.update({
        })
        return context


class HallView(TemplateView):
    template_name = 'demo/hall.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        number = request.POST.get('hall')
        hall = Hall.objects.get(number=number)
        context['select_number'] = number

        x = 5
        y = 1
        result_html = '<table class="table table-hover"><tr><th bgcolor="#E6E6FA">Номер ряда</th>'

        result_html += '<th>э</th><th>к</th><th>р</th><th>а</th><th>н</th>'
        while x <= hall.count_series:
            result_html += '<th></th>'
            x += 1
        result_html += '</tr>'
        x = 1
        while x <= hall.count_series:
            if x % 2 != 0:
                result_html += '<tr><td bgcolor="#E6E6FA" width="30">%s</td>' % str(x)
            else:
                result_html += '<tr><td bgcolor="#D3D3D3" width="30">%s</td>' % str(x)
            while y <= hall.count_place:
                if x % 2 == 0:
                    if (y + 1) % 2 == 0:
                        result_html += '<td bgcolor="#E6E6FA">%s</td>' % str(y)
                    else:
                        result_html += '<td bgcolor="#D3D3D3">%s</td>' % str(y)
                else:
                    if y % 2 == 0:
                        result_html += '<td bgcolor="#E6E6FA">%s</td>' % str(y)
                    else:
                        result_html += '<td bgcolor="#D3D3D3">%s</td>' % str(y)
                y += 1
            result_html += '</tr>'
            x += 1
            y = 1
        result_html += '</html>'
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
    template_name = 'demo/film.html'
    return render_to_response(template_name,
                              RequestContext(request, {
                                  'formadd': FilmModelForm(),
                                  'formedit': form,
                                  "id_session": id,
                                  "list_film": Film.objects.all(),
                                  }))


def delete_film(request, id):
    film_edit_form = FilmModelForm(instance=Film.objects.get(id=1))
    try:
        preferences = Film.objects.get(
            id=id
        )
    except Film.DoesNotExist:
        preferences = None

    preferences.delete()

    if request.method == "POST":
        form = FilmModelForm(data=request.POST,
                             instance=preferences)
        if form.is_valid():
            preferences = form.save()
            if request.is_ajax():
                return HttpResponse('true')
            messages.success(request, 'Фильм удален.')
        elif request.is_ajax():
            return HttpResponse('false')
    else:
        form = FilmModelForm(
            id=id,
            instance=preferences
        )
    template_name = 'demo/film.html'
    return render_to_response(template_name,
                              RequestContext(request, {
                                  'formadd': FilmModelForm(),
                                  'formedit': film_edit_form,
                                  "id_session": id,
                                  "list_film": Film.objects.all(),
                                  }))


class FilmsView(TemplateView):
    template_name = 'demo/film.html'
    film_add_form = FilmModelForm()

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        id = request.POST.get('film')[0:request.POST.get('film').find('/')]
        film = Film.objects.get(id=id)
        context['formadd'] = self.film_add_form
        context['formedit'] = FilmModelForm(instance=film)
        context['id_film'] = id
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(FilmsView, self).get_context_data(**kwargs)

        context.update({
            "formadd": self.film_add_form,
            "list_film": Film.objects.all(),
            })
        return context
