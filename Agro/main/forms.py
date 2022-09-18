from django.forms import ModelForm, TextInput
from .models import Info

class InfoForm(ModelForm):
    class Meta:
        model = Info
        fields = ["vino", "height", "aspect", "slope", "water"]
        widgets = {
            "vino": TextInput(attrs={
                "type": "text",
                "placeholder": "№ виноградников(1 2 3...)",
                "size": "18"
            }),
            "height": TextInput(attrs={
                "type": "text",
                "placeholder": "Введите высоту",
                "size": "18"
            }),
            "aspect": TextInput(attrs={
                "type": "text",
                "placeholder": "Введите экспозицию",
                "size": "18"
            }),
            "slope": TextInput(attrs={
                "type": "text",
                "placeholder": "Введите уклон мест.",
                "size": "18"
            }),
            "water": TextInput(attrs={
                "type": "text",
                "placeholder": "Время затопления",
                "size": "18"
            }),
        }