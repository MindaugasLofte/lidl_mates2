from .models import MyUser, Profilis
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