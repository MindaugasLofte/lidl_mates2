from django.db import models

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
    zone_code = models.CharField(max_length=80, choices=zone_choices, default='40', help_text='Darbo zona sandėlyje',
    blank=True)
    zone_description=models.CharField(max_length=80, help_text='Zonos aprasymas pvz 60-Tiko')

    def __str__(self):
        return self.zone_code

class Darbuotojas (models.Model):
    """modelis reprezentuojantis darbuotoja."""
    picker_code = models.CharField(help_text='rinkejo_kodas', max_length=3)
    first_name = models.CharField(help_text='Vardas', max_length=80)
    last_name = models.CharField(help_text='Pavardė', max_length=80)
    working_zone = models.ForeignKey('Darbo_zona_sandelyje', null=True, on_delete=models.SET_NULL)
    position_choices = (
        ('grupes vadovas','grupes vadovas'),
        ('grupes vadovo asistentas', 'grupes vadovo asistentas'),
        ('grupes vadovo asistentas', 'grupes vadovo asistentas'),
        ('prekiu komplektuotojas', 'prekiu komplektuotojas'))
    position = models.CharField(max_length=80, choices=position_choices, default='prekiu komplektuotojas', help_text='Darbuotojo pareigos',blank=True)
    photo = models.ImageField(help_text='Darbuotojo foto arba avataras', upload_to='photos', null=True)
    working_since = models.DateField(help_text='Darbo pradžia LIDL imoneje', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    # def get_absolute_url(self):
    #     """Nurodo  darbuotojo galutinį adresą"""
    #     return reverse('darbuotojas-detail', args=[str(self.id)])
    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Darbo_laiko_irasai(models.Model):
    """modelis reprezentuojantis darbo laiko irasa
    galimi variantai:darbas, pertrauka arba pietu peretrauka.
    """
    data = models.DateField(help_text='kada dirbta', null=True, blank=True)
    working_zone = models.ForeignKey('Darbo_zona_sandelyje',max_length=80, null=True, on_delete=models.SET_NULL)
    darbuotojas = models.ForeignKey('Darbuotojas',max_length=100, null=True, on_delete=models.SET_NULL)
    work_status = (
        ('darbas','darbas'),
        ('pertrauka','pertrauka'),
        ('pietu pertrauka','pietu pertrauka'))
    status = models.CharField(help_text='Darbo grafiko laiko tipas', max_length=40, choices= work_status, default='darbas', blank=True)
    duration = models.DurationField(help_text='darbo iraso trukme', null=True, blank=True)
    picked_boxes = models.IntegerField(help_text='Surinkta deziu per irasa')
    class Meta:
        ordering = ['data']

    def __str__(self):
        return f'{self.data} diena darbuotojas, kurio rinkejo kodas{self.darbuotojas.picker_code} surinko {self.picked_boxes} dezes'


class Darbo_grafikas_planas(models.Model):
    """modelis reprezentuojantis darbo grafiko plana, kiek kuris darbuotojas dirbs.
    """
    data = models.DateField(help_text='kada dirbs', null=True, blank=True)
    day_choices = (
        ('darbas', 'darbas'),
        ('laisvadienis', 'laisvadienis'),
        ('atostogos', 'atostogos'),
        ('mamadienis', 'mamadienis'),
        ('nedarbiningumas', 'nedarbiningumas'),
        ('nedarbo diena', 'nedarbo diena'),
        ('karine tarnyba', 'karine tarnyba'),
        ('idirbis kitame skyriuje', 'idirbis kitame skyriuje'))
    day_status = models.CharField(help_text='Dienos statusas', max_length=40, choices=day_choices, default='darbas', blank=True)

    working_zone = models.ForeignKey('Darbo_zona_sandelyje',max_length=80, null=True, on_delete=models.SET_NULL)
    darbuotojas = models.ForeignKey('Darbuotojas',max_length=100, null=True, on_delete=models.SET_NULL)
    position_choices = (
        ('grupes vadovas', 'grupes vadovas'),
        ('grupes vadovo asistentas', 'grupes vadovo asistentas'),
        ('grupes vadovo asistentas', 'grupes vadovo asistentas'),
        ('prekiu komplektuotojas', 'prekiu komplektuotojas'))
    position = models.CharField(max_length=80, choices=position_choices, default='prekiu komplektuotojas',help_text='Darbuotojo pareigos',blank=True)
    shift_choices = (
        ('8', '100% etatas -8val'),
        ('6', '75% etatas -6val'),
        ('4', '50% etatas -4val'))
    shift_status = models.CharField(help_text='Darbo status', max_length=40, choices=shift_choices, default='8', blank=True)

    class Meta:
        ordering = ['data','darbuotojas']

    def __str__(self):
        return f'{self.data} - {self.darbuotojas} - {self.shift_status} '


class Notes(models.Model):
    data = models.DateField(help_text='kada zinute sukurta', null=True, blank=True)
    darbuotojas = models.ForeignKey('Darbuotojas', null=True, on_delete=models.SET_NULL)
    notes_choices = (
        ('9', 'paprasta zinute sau'),
        ('0', 'reikia informuoti tiesiogini vadova'), #0 statusas bus isrikiuota auksciausiai
        ('8', 'metu ideja'))
    note_type = models.CharField(help_text='Zinutes tipas', max_length=40, choices=notes_choices, default='9', blank=True)
    summary = models.TextField(max_length=1000, help_text='Svarbu aprasyti placiau, aciu uz jusu laika.')

    class Meta:
        ordering = ['note_type','data']
    def __str__(self):
        return f'{self.note_type} - {self.data} - {self.darbuotojas} '


class Krautuvas(models.Model):
    krautuvo_id = models.IntegerField(help_text='krautuvo numeris')
    data_taken = models.DateField(help_text='kada krautuvas paiimtas', null=True, blank=True)
    darbuotojas = models.ForeignKey('Darbuotojas', null=True, on_delete=models.SET_NULL)
    notes_choices = (
        ('aukstas', 'aukstas'),
        ('vidutinis', 'vidutinis'),
        ('zemas', 'zemas'),
        ('be pastebejimu', 'be pastebejimu'))
    note_type = models.CharField(help_text='Rasto gedimo/pastabos svarba', max_length=40, choices=notes_choices, default='be pastebejimu',
                                 blank=True)
    notes = models.TextField(max_length=1000, help_text='labai svarbu pamineti ir smulkiausius gedimus, dekojame.')

    class Meta:
        ordering = ['data_taken','note_type']
        verbose_name_plural = "krautuvai"

    def __str__(self):
        return f'{self.krautuvo_id} krautuva {self.data_taken} diena  naudojosi {self.darbuotojas} '









    


