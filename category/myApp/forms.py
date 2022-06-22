from django import forms

class HotspotForm(forms.ModelForm):
    class Meta:
        model = hotspot
        fields = "__all__"