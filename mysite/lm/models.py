from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
# from django.contrib.auth.models import User
import datetime as dt
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from PIL import Image
from tinymce.models import HTMLField
# Create your models here.
# jeigu reikia rinktis vbalandini duration
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 16)]
class Darbo_zona_sandelyje (models.Model):
    """modelis reprezentuojantis zonos numerį ir pavadinimą."""
    zone_choices = (
        ('20','20 - HR'),
        ('40','40 - MOPRO'),
        ('41', '41 - Pienas'),
        ('60', '60 - TIKO'),
        ('61', '61 - BakeOff'),
        ('70', '70 - Fruits'),
        ('50', '50 - Mėsa'),
        ('90', '90 - NonFood')
        )
    zone_code = models.CharField(_('Working zone code'), max_length=80, choices=zone_choices, default='40', help_text='Darbo zona sandėlyje',
    blank=True, unique=True)
    zone_description=models.CharField(_('Description'), max_length=80, help_text='Zonos aprasymas pvz 60-Tiko')
    class Meta:
        ordering = ['zone_code']
        verbose_name = _("Working zone")
        verbose_name_plural = _("Working zones")
    def __str__(self):
        return f'{self.zone_code}'
# custom user
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, picker_code=None, date_of_birth=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            picker_code=picker_code,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            # date_of_birth=date_of_birth,
            # picker_code=picker_code,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(null=True, blank=True,)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth', 'picker_code']

    picker_code = models.CharField(_('Piker code'),help_text='rinkejo_kodas', max_length=3, unique=True)
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
    photo = models.ImageField(help_text='Darbuotojo foto arba avataras', upload_to='profile_pics', null=True, blank=True, default='default.png')
    working_since = models.DateField(_('Working since'),help_text='Darbo pradžia LIDL imoneje', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _("Worker")
        verbose_name_plural = _("Workers")

    # def get_absolute_url(self):
    #     """Nurodo  darbuotojo galutinį adresą"""
    #     return reverse('darbuotojas-detail', args=[str(self.id)])
    # def __str__(self):
    #     return f'{self.last_name} {self.first_name}'


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def when_salary_increase(self):
        if self.working_since:
            dirbo_dienu = (dt.date.today() - self.working_since).days
            # max_riba_algu_kelimui 3metai arba 1095d
            if dirbo_dienu >=1095:
                return f"Pasiekėte maksimalią III pakopą savo darbo pozicijoje. Norint gauti didesnę algą, turite prisiimti naujų iššūkių ir kilti karjeros laiptais!"
            elif dirbo_dienu < 1095 and dirbo_dienu >= 730:
                atimame_2metus=dirbo_dienu-730
                return f"Esate II pakopoje savo darbo pozicijoje. Planuojamas atlyginimo kėlimas už {atimame_2metus} dienų!"
            elif dirbo_dienu < 730 and dirbo_dienu >= 365:
                atimame_1metus=dirbo_dienu-365
                return f"Esate I pakopoje savo darbo pozicijoje. Planuojamas atlyginimo kėlimas už {atimame_1metus} dienų!"
            else:
                return f"kažkas negerai"


class Darbo_laiko_irasai(models.Model):
    """modelis reprezentuojantis darbo laiko irasa
    galimi variantai:darbas, pertrauka arba pietu peretrauka.
    """
    data = models.DateField(_('Date of working record'), help_text='kada dirbta', null=True, blank=True)
    working_zone = models.ForeignKey('Darbo_zona_sandelyje', max_length=80, null=True, on_delete=models.SET_NULL)
    darbuotojas = models.ForeignKey('MyUser',max_length=100, null=True, on_delete=models.SET_NULL)
    work_status = (
        ('darbas','darbas'),
        ('pertrauka','pertrauka'),
        ('pietu pertrauka','pietu pertrauka'))
    status = models.CharField(_('Type of working record'), help_text='Darbo grafiko laiko tipas', max_length=40, choices= work_status, default='darbas', blank=True)
    duration = models.CharField(_('Duration'), help_text='darbo iraso trukme', null=True, blank=True, default=dt.timedelta(hours=7), max_length=20)
    picked_boxes = models.IntegerField(_('Picked boxes per duration'), help_text='Surinkta deziu per irasa', null=True, blank=True,default='0')
    class Meta:
        ordering = ['data']
        verbose_name = _("Working record")
        verbose_name_plural = _("Working records")
    def get_absolute_url(self):
        """Nurodo  darbo iraso galutinį adresą"""
        return reverse('Darbo_laiko_irasai', args=[str(self.id)])

    # def __str__(self):
    #     return f'{self.data} diena darbuotojas, kurio rinkejo kodas{self.darbuotojas.picker_code} surinko {self.picked_boxes} dezes'
    # @property
    # def pick_rate_per_hour(self):
    #     if self.duration and self.picked_boxes:
    #         return self.picked_boxes/int(float(self.duration))

    def __str__(self):
        return f'{self.data} - {self.darbuotojas} - {self.working_zone.zone_code} - {self.status}  - {self.duration} - {self.picked_boxes}'


class Notes(models.Model):
    data = models.DateField(_('Date'), help_text='kada zinute sukurta', null=True, blank=True)
    darbuotojas = models.ForeignKey('MyUser', null=True, on_delete=models.SET_NULL)
    notes_choices = (
        ('9', 'paprasta zinute sau'),
        ('0', 'reikia informuoti tiesiogini vadova'), #0 statusas bus isrikiuota auksciausiai
        ('8', 'metu ideja'))
    note_type = models.CharField(_('Type of notes'), help_text='Zinutes tipas', max_length=40, choices=notes_choices, default='9', null=True, blank=True)
    summary = HTMLField(help_text='Rašykite ką norite!kiti varotojai nematys jusu zinutes', null=True, blank=True)

    class Meta:
        ordering = ['data', 'note_type']
        verbose_name = _("Note")
        verbose_name_plural = _('Notes')
    def __str__(self):
        return f'{self.note_type} - {self.data} - {self.darbuotojas} '


class Krautuvas(models.Model):
    krautuvo_id = models.IntegerField(_('Vechiles ID "3 digits"'), help_text='krautuvo numeris', unique=False)
    data_taken = models.DateField(_('Date when vechiles was taken'), help_text='kada krautuvas paiimtas', null=True, blank=True)
    darbuotojas = models.ForeignKey('MyUser',null=True, on_delete=models.SET_NULL,blank=True)
    LOAN_STATUS = (
        (_('ready'), _('ready')),
        ('taken', 'taken'),
        ('waiting_for_repair', 'waiting_for_repair'),
        ('repairing', 'repairing')
    )
    status = models.CharField(_('Status'), max_length=30, choices=LOAN_STATUS, default='taken', help_text='Status', null=True, blank=True)
    notes_choices = (
        ('aukstas', 'aukstas'),
        ('vidutinis', 'vidutinis'),
        ('zemas', 'zemas'),
        ('be pastebejimu', 'be pastebejimu'))
    note_type = models.CharField(_('Importance of the notes'), help_text='Rasto gedimo/pastabos svarba', max_length=40, choices=notes_choices, default='be pastebejimu',
                                 null=True, blank=True)

    notes = HTMLField(help_text='labai svarbu pamineti ir smulkiausius gedimus, dekojame.', null=True, blank=True)

    class Meta:
        ordering = ['krautuvo_id']
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")

    def get_absolute_url(self):
        """Nurodo  krautuvo galutinį adresą"""
        return reverse('Darbo_laiko_irasai', args=[str(self.id)])

    def __str__(self):
        return f'{self.krautuvo_id} krautuvą {self.data_taken} dieną  naudojosi {self.darbuotojas} '

class Profilis(models.Model):
    # cascade sako, kad jei istrinsiu vartotoja ir profilis issitrins
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    # default.png turi buti library-media folderyje
    photo = models.ImageField(default='default.png', upload_to='profile_pics', null=True) #media-profile_pics kataloge jas saugos
    # cia jei bus vienaskaita arba daugiskaita, pagal tai nurodys
    class Meta:
        verbose_name = 'Profilis'
        verbose_name_plural = 'Profiliai'
    def __str__(self):
        return f"{self.user.email} profilis"

# 1114paskaitos 2v kad matytusi nuotraukos vienodo dydzio
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

