from django.contrib import admin
from . models import MyUser, Darbo_laiko_irasai, Darbo_zona_sandelyje, Notes, Krautuvas
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
# Register your models here.


class KrautuvasAdmin(admin.ModelAdmin):
    list_display = ("krautuvo_id", "data_taken", "darbuotojas", "note_type", "status")
    list_filter = ('note_type', 'status')
    # jeigu norime pasirinkti foreign key reiksme, reikia __ ir tada atributa
    search_fields = ('krautuvo_id', 'status',"darbuotojas__first_name","darbuotojas__last_name")


class Darbo_zona_sandelyjeAdmin(admin.ModelAdmin):
    list_display = ("zone_code", "zone_description")


# class DarbuotojasAdmin(admin.ModelAdmin):
#     list_display = ("picker_code", "first_name", "last_name",  "working_department", "working_zone", "position", "working_since")
#     list_filter = ('working_zone', 'working_department')
#     search_fields = ('picker_code', 'last_name','first_name')


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

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['email', 'date_of_birth']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'date_of_birth', 'is_active', 'is_admin','picker_code']


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'date_of_birth', 'is_admin','picker_code',"first_name", "last_name",  "working_department", "working_zone", "position", "working_since",'photo']
    list_filter = ['is_admin','working_zone', 'working_department']
    fieldsets = [
        ("Login fields", {'fields': ['email', 'password']}),
        ('Personal info', {'fields': ["first_name", "last_name",'date_of_birth','photo']}),
        ('Work info', {'fields': ['picker_code',  "working_department", "working_zone", "position", "working_since"]}),
        ('Permissions', {'fields': ['is_admin']}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'date_of_birth', 'password1', 'password2','picker_code',"first_name", "last_name",  "working_department", "working_zone", "position", "working_since",'photo'],
        }),
    ]
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = []


admin.site.register(MyUser, UserAdmin)
admin.site.register(Darbo_laiko_irasai, Darbo_laiko_irasaiAdmin)
admin.site.register(Darbo_zona_sandelyje, Darbo_zona_sandelyjeAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(Krautuvas, KrautuvasAdmin)


# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
