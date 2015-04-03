from django.contrib import admin
from demo.models import Place, Session, Hall, Film


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('status',
                    'number_place',
                    'number_series',
                    'price')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('status',
                    'get_hall',
                    'get_film',
                    'date_time',
                    'time_session')

    def get_hall(self, obj):
        return obj.hall.number
    get_hall.short_description = 'Hall'

    def get_film(self, obj):
        return obj.film.film
    get_film.short_description = 'Film'


class HallAdmin(admin.ModelAdmin):
    list_display = ('number',
                    'count_place',
                    'count_series',)


class FilmAdmin(admin.ModelAdmin):
    list_display = ('film', )

admin.site.register(Place, PlaceAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Film, FilmAdmin)