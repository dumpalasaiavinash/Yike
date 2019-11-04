from django import forms
class msgForm(forms.Form):
    msg=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'autocomplete':'off','onfocus':'stats()','onblur':'stats2()'}),required=False)
    img=forms.FileField(widget=forms.FileInput(attrs={'style':'display:none','accept':'images/*'}),required=False)
