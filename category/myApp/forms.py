from django import forms
from .models import CommentFestival


# class HotspotForm(forms.ModelForm):
#     class Meta:
#         model = hotspot
#         fields = "__all__"


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentFestival
        exclude = ('festival', 'created_at')
        widgets = {
            'username': forms.TextInput(attrs={
                'value': 'ㅇㅇ'
            }),
            'passwd': forms.TextInput(attrs={
                'type': 'password',
                'value': '1234',
            }),
            'content': forms.Textarea(attrs={
                'cols': '60',
                'rows': '4'
            })
        }
