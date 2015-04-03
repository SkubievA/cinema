# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class Film(models.Model):
    film = models.CharField(max_length=50,
                            verbose_name=_(u'Название фильма'))

    class Meta:
        verbose_name = _(u'Фильм')
        verbose_name_plural = _(u'Фильмы')
        db_table = 'films'


class Hall(models.Model):
    number = models.IntegerField(verbose_name=_(u'Номер зала'))
    count_place = models.IntegerField(verbose_name=_(u'Количество мест в ряде'))
    count_series = models.IntegerField(verbose_name=_(u'Количество рядов'))

    class Meta:
        verbose_name = _(u'Зал')
        verbose_name_plural = _(u'Залы')
        db_table = 'halls'


class Session(models.Model):
    statuses = [
        (0, _(u'Актуально')),
        (1, _(u'Не актуально')),
    ]
    status = models.IntegerField(verbose_name=_(u'Статус'),
                                 choices=statuses)
    hall = models.ForeignKey(Hall,
                             verbose_name=_(u'Зал'))
    film = models.ForeignKey(Film,
                             verbose_name=_(u'Фильм'))
    date_time = models.DateTimeField(verbose_name=_(u'Дата и время начала сеанса'),
                                     default=timezone.now())
    time_session = models.IntegerField(verbose_name=_(u'Время сеанса'))

    class Meta:
        verbose_name = _(u'Сеанс')
        verbose_name_plural = _(u'Сенсы')
        db_table = 'sessions'


class Place(models.Model):
    statuses = [
        (0, _(u'Свободно')),
        (1, _(u'Занято')),
    ]
    status = models.IntegerField(verbose_name=_(u'Статус'),
                                 default=False,
                                 choices=statuses)
    session = models.ForeignKey(Session,
                                verbose_name=_(u'Сеанс'))
    number_place = models.IntegerField(verbose_name=_(u'Номер места'))
    number_series = models.IntegerField(verbose_name=_(u'Номер ряда'))
    price = models.IntegerField(verbose_name=_(u'Цена'))

    class Meta:
        verbose_name = _(u'Место')
        verbose_name_plural = _(u'Места')
        db_table = 'places'