from django import forms
from .models import Control, Config
        
class ControlForm(forms.ModelForm):
    class Meta:
        model = Control
        fields = ['level','image']

class ConfigForm(forms.ModelForm):
    whatsapp_number = forms.IntegerField(label='WhatsApp Number',widget=forms.NumberInput(
        attrs={
            'class':'form-control',
            'placeholder':'234XXXXXXXXXX',
        }
    ))
    class Meta:
        model = Config
        fields = ['whatsapp_number']