from django import forms
from .models import UserInput

class UserInputForm(forms.ModelForm):
    class Meta:
        model = UserInput
        fields = ['proteins', 'carbohydrates', 'fat']
        widgets = {
            'proteins': forms.TextInput(attrs={'class': 'text'}),
            'carbohydrates' : forms.TextInput(attrs={'class' : 'text'}),
            'fat' : forms.TextInput(attrs={'class':'text'}),
        }
