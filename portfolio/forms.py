from django import forms

class UploadFormFile(forms.Form):
    file = forms.FileField()