from django import forms

class TextAnalysisForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

class PdfAnalysisForm(forms.Form):
    pdf_file = forms.FileField()

class VoiceAnalysisForm(forms.Form):
    audio_file = forms.FileField()