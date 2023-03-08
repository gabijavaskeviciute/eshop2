from django.contrib import admin

from .models import Preke, Uzsakymas, Uzsakymo_eilute, Siuntimas, Profilis


class Uzsakymo_eiluteInline(admin.TabularInline):
    model = Uzsakymo_eilute
    extra = 0
    list_display =('uzsakymas', 'preke', 'kiekis')


class Uzsakymo_eiluteAdmin(admin.ModelAdmin):
    list_display = ('uzsakymas', 'preke', 'kiekis', 'kaina')

class PrekesAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')

class UzsakymaiAdmin(admin.ModelAdmin):
    inlines = [Uzsakymo_eiluteInline]
    list_display = ('preke_id', 'uzsakymo_numeris', 'vartotojas')




admin.site.register(Preke, PrekesAdmin)
admin.site.register(Uzsakymas, UzsakymaiAdmin)
admin.site.register(Uzsakymo_eilute, Uzsakymo_eiluteAdmin)
admin.site.register(Profilis)
