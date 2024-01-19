from django import forms
from core.models import Assets, AssetsType, APIConnections, ImportFile


class APIForm(forms.Form):
    asset = forms.ModelChoiceField(queryset=Assets.objects.all(), required=False, label=("Ativos"))
    asset_type = forms.ModelChoiceField(queryset=AssetsType.objects.all(), required=False, label=("Tipo de Ativo"))
    site = forms.ModelChoiceField(queryset=APIConnections.objects.all(), required=False, label=("Site"))

    def __str__(self):
        return "APIForm"

class ImportForm(forms.ModelForm):
    file = forms.FileField(label="Arquivo")
    
    class Meta:
        model = ImportFile
        fields = ['file']