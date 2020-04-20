from django import forms


class RSSSourcesFileForm(forms.Form):
    source_file = forms.FileField()
