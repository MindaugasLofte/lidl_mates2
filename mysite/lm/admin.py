from django.contrib import admin
from . models import Darbuotojas, Darbo_laiko_irasai, Darbo_zona_sandelyje, Notes, Krautuvas
# Register your models here.


class KrautuvasAdmin(admin.ModelAdmin):
    list_display = ("krautuvo_id", "data_taken", "darbuotojas", "note_type", "status")
    list_filter = ('note_type', 'status')
    # jeigu norime pasirinkti foreign key reiksme, reikia __ ir tada atributa
    search_fields = ('krautuvo_id', 'status',"darbuotojas__first_name","darbuotojas__last_name")


class Darbo_zona_sandelyjeAdmin(admin.ModelAdmin):
    list_display = ("zone_code", "zone_description")


class DarbuotojasAdmin(admin.ModelAdmin):
    list_display = ("picker_code", "first_name", "last_name",  "working_department", "working_zone", "position", "working_since")
    list_filter = ('working_zone', 'working_department')
    search_fields = ('picker_code', 'last_name','first_name')


class Darbo_laiko_irasaiAdmin(admin.ModelAdmin):
    list_display = ("data", "status", "working_zone", "darbuotojas", "data", "duration", "picked_boxes")
    list_filter = ('working_zone', 'data', 'status')
    search_fields = ["darbuotojas__first_name","darbuotojas__last_name"]


class NotesAdmin(admin.ModelAdmin):
    list_display = ("data", "darbuotojas",  "note_type", "summary")
    list_filter = ('note_type', 'data')
    search_fields = ("darbuotojas__first_name","darbuotojas__last_name")
    fieldsets = (
        (None, {'fields': ('data', 'darbuotojas')}),
        ('Note information', {'fields': ('note_type', 'summary')}),
    )

admin.site.register(Darbuotojas, DarbuotojasAdmin)
admin.site.register(Darbo_laiko_irasai, Darbo_laiko_irasaiAdmin)
admin.site.register(Darbo_zona_sandelyje, Darbo_zona_sandelyjeAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(Krautuvas, KrautuvasAdmin)
