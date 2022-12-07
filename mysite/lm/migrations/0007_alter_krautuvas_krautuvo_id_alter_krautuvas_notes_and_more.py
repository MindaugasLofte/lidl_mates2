# Generated by Django 4.1.3 on 2022-12-06 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('lm', '0006_alter_notes_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='krautuvas',
            name='krautuvo_id',
            field=models.IntegerField(help_text='krautuvo numeris', verbose_name='Vechiles ID "3 digits"'),
        ),
        migrations.AlterField(
            model_name='krautuvas',
            name='notes',
            field=tinymce.models.HTMLField(blank=True, help_text='labai svarbu pamineti ir smulkiausius gedimus, dekojame.', null=True),
        ),
        migrations.AlterField(
            model_name='notes',
            name='summary',
            field=tinymce.models.HTMLField(blank=True, help_text='Rašykite ką norite!kiti varotojai nematys jusu zinutes', null=True),
        ),
        migrations.CreateModel(
            name='TakeMachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('data_taken', models.DateField(blank=True, help_text='kada krautuvas paiimtas', null=True, verbose_name='Date when vechiles was taken')),
                ('krautuvo_id', models.IntegerField(help_text='krautuvo numeris', verbose_name='Vechiles ID "3 digits"')),
                ('status', models.CharField(blank=True, choices=[('ready', 'ready'), ('taken', 'taken'), ('waiting_for_repair', 'waiting_for_repair'), ('repairing', 'repairing')], default='taken', help_text='Status', max_length=30, null=True, verbose_name='Status')),
                ('note_type', models.CharField(blank=True, choices=[('aukstas', 'aukstas'), ('vidutinis', 'vidutinis'), ('zemas', 'zemas'), ('be pastebejimu', 'be pastebejimu')], default='be pastebejimu', help_text='Rasto gedimo/pastabos svarba', max_length=40, null=True, verbose_name='Importance of the notes')),
                ('notes', tinymce.models.HTMLField(blank=True, help_text='labai svarbu pamineti ir smulkiausius gedimus, dekojame.', null=True)),
                ('darbuotojas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('machine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lm.krautuvas')),
            ],
        ),
    ]