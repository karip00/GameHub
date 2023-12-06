from django import forms
from .models import Game, Genre
from tinymce.widgets import TinyMCE

class GenreCreateForm(forms.ModelForm):
    class Meta:
        model = Genre

        fields = [
            "title",
            "subtitle",
            "slug",
            "image",
        ]

class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game

        fields = [
            "title",
            "subtitle",
            "game_slug",
            "content",
            "notes",
            "genre",
            "image",
        ]

class GenreUpdateForm(forms.ModelForm):
    class Meta:
        model = Genre

        fields = [
            "title",
            "subtitle",
            "image",
        ]

class GameUpdateForm(forms.ModelForm):
    class Meta:
        model = Game

        fields = [
            "title",
            "subtitle",
            "content",
            "notes",
            "genre",
            "image",
            "price"
        ]

class NewsletterForm(forms.Form):
    subject = forms.CharField()
    receivers = forms.CharField()
    message = forms.CharField(widget=TinyMCE(), label="Email content")