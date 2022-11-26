from django.contrib import admin
from . models import Darbuotojas, Darbo_laiko_irasai, Darbo_zona_sandelyje, Notes, Krautuvas
# Register your models here.


class KrautuvasAdmin(admin.ModelAdmin):
    list_display = ("krautuvo_id", "data_taken",)

admin.site.register(Darbuotojas)
admin.site.register(Darbo_laiko_irasai)
admin.site.register(Darbo_zona_sandelyje)
admin.site.register(Notes)
admin.site.register(Krautuvas, KrautuvasAdmin)

