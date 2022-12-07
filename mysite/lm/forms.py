from .models import MyUser, Profilis, Krautuvas, Notes,Darbo_laiko_irasai
from django import forms

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = MyUser
        fields = [ "first_name", "last_name", 'email', 'picker_code', "working_department", "working_zone", "position", "working_since",'date_of_birth']

class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['photo']


class DateInput(forms.DateInput):
    input_type = 'date'


class UserKrautuvasCreateForm(forms.ModelForm):
    class Meta:
        model = Krautuvas
        fields = ("data_taken", "krautuvo_id", "darbuotojas", "note_type", "status", 'notes',)
        widgets = {'darbuotojas': forms.HiddenInput(), 'data_taken': DateInput()}



# class UserNotesCreateForm(forms.ModelForm):
#     class Meta:
#         model = Notes
#         fields = ("data", "darbuotojas", "note_type", "summary",)
#         widgets = {'darbuotojas': forms.HiddenInput(), 'data': DateInput()}
#
# class UserWorkingRecordCreateForm(forms.ModelForm):
#     class Meta:
#         model = Darbo_laiko_irasai
#         fields = ("data", 'working_zone', "darbuotojas", 'status', 'duration', "picked_boxes")
#         widgets = {'darbuotojas': forms.HiddenInput(), 'data': DateInput()}








