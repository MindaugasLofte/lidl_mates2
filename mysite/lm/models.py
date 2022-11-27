from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.
# ateiciai
# HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
class Darbo_zona_sandelyje (models.Model):
    """modelis reprezentuojantis zonos numerį ir pavadinimą."""
    zone_choices = (
        ('20','20 - HR'),
        ('40','40 - MOPRO'),
        ('41', '41 - Pienas'),
        ('60', '60 - TIKO'),
        ('61', '61 - BakeOff'),
        ('70', '70 - Fruits'),
        ('80', '80 - Mėsa'),
        ('90', '90 - NonFood')
        )
    zone_code = models.CharField(_('Working zone code'), max_length=80, choices=zone_choices, default='40', help_text='Darbo zona sandėlyje',
    blank=True)
    zone_description=models.CharField(_('Description'),max_length=80, help_text='Zonos aprasymas pvz 60-Tiko')
    class Meta:
        ordering = ['zone_code']
        verbose_name = _("Working zone")
        verbose_name_plural = _("Working zones")
    def __str__(self):
        return f'{self.zone_code} - {self.zone_description}'

class Darbuotojas (models.Model):
    """modelis reprezentuojantis darbuotoja."""
    picker_code = models.CharField(_('Piker code'),help_text='rinkejo_kodas', max_length=3)
    first_name = models.CharField(_('First name'),help_text='Vardas', max_length=80)
    last_name = models.CharField(_('Last name'),help_text='Pavardė', max_length=80)
    working_zone = models.ForeignKey('Darbo_zona_sandelyje',null=True, on_delete=models.SET_NULL)
    working_department_choices = (
        ('Vilniaus apsk', 'Vilniaus apsk'),
        ('Vilniaus regioninis sandėlys', 'Vilniaus regioninis sandėlys'),
        ('Kauno apsk', 'Kauno apsk'),
        ('Kauno regioninis sandėlys', 'Kauno regioninis sandėlys'),
        ('Klaipėdos apsk', 'Klaipėdos apsk'),
    )
    working_department = models.CharField(_('Working disctric or logistic warehouse'),max_length=80, choices=working_department_choices, default='Kauno regioninis sandėlys',
                                help_text='Kurioje (-iame) apskrityje/logistikos sandėlyje dirbate', blank=True)
    position_choices = (
        ('grupes vadovas','grupes vadovas'),
        ('grupes vadovo asistentas', 'grupes vadovo asistentas'),
        ('grupes vadovo asistentas', 'grupes vadovo asistentas'),
        ('prekiu komplektuotojas', 'prekiu komplektuotojas'))
    position = models.CharField(_('Working position'),max_length=80, choices=position_choices, default='prekiu komplektuotojas', help_text='Darbuotojo pareigos',blank=True)
    photo = models.ImageField(help_text='Darbuotojo foto arba avataras', upload_to='photos', null=True)
    working_since = models.DateField(_('Working since'),help_text='Darbo pradžia LIDL imoneje', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _("Worker")
        verbose_name_plural = _("Workers")

    # def get_absolute_url(self):
    #     """Nurodo  darbuotojo galutinį adresą"""
    #     return reverse('darbuotojas-detail', args=[str(self.id)])
    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Darbo_laiko_irasai(models.Model):
    """modelis reprezentuojantis darbo laiko irasa
    galimi variantai:darbas, pertrauka arba pietu peretrauka.
    """
    data = models.DateField(_('Date of working record'),help_text='kada dirbta', null=True, blank=True)
    working_zone = models.ForeignKey('Darbo_zona_sandelyje',max_length=80, null=True, on_delete=models.SET_NULL)
    darbuotojas = models.ForeignKey('Darbuotojas',max_length=100, null=True, on_delete=models.SET_NULL)
    work_status = (
        ('darbas','darbas'),
        ('pertrauka','pertrauka'),
        ('pietu pertrauka','pietu pertrauka'))
    status = models.CharField(_('Type of working record'),help_text='Darbo grafiko laiko tipas', max_length=40, choices= work_status, default='darbas', blank=True)
    duration = models.DurationField(_('Duration'),help_text='darbo iraso trukme', null=True, blank=True)
    picked_boxes = models.IntegerField(_('Picked boxes per duration'),help_text='Surinkta deziu per irasa')
    class Meta:
        ordering = ['data']
        verbose_name = _("Working record")
        verbose_name_plural = _("Working records")

    def __str__(self):
        return f'{self.data} diena darbuotojas, kurio rinkejo kodas{self.darbuotojas.picker_code} surinko {self.picked_boxes} dezes'


    def __str__(self):
        return f'{self.data} - {self.darbuotojas} - {self.working_zone.zone_code} - {self.status}  - {self.duration} - {self.picked_boxes}'


class Notes(models.Model):
    data = models.DateField(_('Date'),help_text='kada zinute sukurta', null=True, blank=True)
    darbuotojas = models.ForeignKey('Darbuotojas', null=True, on_delete=models.SET_NULL)
    notes_choices = (
        ('9', 'paprasta zinute sau'),
        ('0', 'reikia informuoti tiesiogini vadova'), #0 statusas bus isrikiuota auksciausiai
        ('8', 'metu ideja'))
    note_type = models.CharField(_('Type of notes'),help_text='Zinutes tipas', max_length=40, choices=notes_choices, default='9', blank=True)
    summary = models.TextField(_('Description of the notes'),max_length=1000, help_text='Svarbu aprasyti placiau, aciu uz jusu laika.')

    class Meta:
        ordering = ['data', 'note_type']
        verbose_name = _("Note")
        verbose_name_plural = _('Notes')
    def __str__(self):
        return f'{self.note_type} - {self.data} - {self.darbuotojas} '


class Krautuvas(models.Model):
    krautuvo_id = models.IntegerField(_('Vechiles ID "3 digits"'),help_text='krautuvo numeris')
    data_taken = models.DateField(_('Date when vechiles was taken'),help_text='kada krautuvas paiimtas', null=True, blank=True)
    darbuotojas = models.ForeignKey('Darbuotojas',null=True, on_delete=models.SET_NULL)
    notes_choices = (
        ('aukstas', 'aukstas'),
        ('vidutinis', 'vidutinis'),
        ('zemas', 'zemas'),
        ('be pastebejimu', 'be pastebejimu'))
    note_type = models.CharField(_('Importance of the notes'),help_text='Rasto gedimo/pastabos svarba', max_length=40, choices=notes_choices, default='be pastebejimu',
                                 blank=True)
    notes = models.TextField(max_length=1000, help_text='labai svarbu pamineti ir smulkiausius gedimus, dekojame.')
    LOAN_STATUS = (
        (_('ready'), _('ready')),
        ('taken', 'taken'),
        ('waiting_for_repair', 'waiting_for_repair'),
        ('repairing', 'repairing')
    )
    status = models.CharField(_('Status'), max_length=30, choices=LOAN_STATUS, default='taken', help_text='Status', blank=True)


    class Meta:
        ordering = ['krautuvo_id']
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")

    def __str__(self):
        return f'{self.krautuvo_id} krautuvą {self.data_taken} dieną  naudojosi {self.darbuotojas} '









    


