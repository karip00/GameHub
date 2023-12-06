from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from embed_video.fields import EmbedVideoField
import os 

class Genre(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Genre', slugify(self.slug), instance)
        return None
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="", blank=True) 
    slug = models.SlugField("Genre slug", null=False, blank=False, unique=True)
    published = models.DateTimeField("Date published", default=timezone.now)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    image = models.ImageField(default='default/no_image.jpg', upload_to=image_upload_to, max_length=255)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Genre"
        ordering = ['-published']

class Game(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Genre', slugify(self.genre.slug), slugify(self.game_slug), instance)
        return None
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="", blank=True)
    game_slug = models.SlugField("Game slug", null=False, blank=False, unique=True)
    content = HTMLField(blank=True, default="")
    notes = HTMLField(blank=True, default="")
    published = models.DateTimeField("Date published", default=timezone.now)
    modified = models.DateTimeField("Date modified", default=timezone.now)
    genre = models.ForeignKey(Genre, default="", verbose_name="Series", on_delete=models.SET_DEFAULT)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    image = models.ImageField(default='default/no_image.jpg', upload_to=image_upload_to, max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    video = EmbedVideoField()

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return self.genre.slug + "/" + self.game_slug

    class Meta:
        verbose_name_plural = "Game"
        ordering = ['-published']