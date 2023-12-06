from django.contrib import admin
from  embed_video.admin  import  AdminVideoMixin
from .models import Game, Genre

class GenreAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'slug', 'author', 'image',]

class GameAdmin(AdminVideoMixin, admin.ModelAdmin):
    fieldsets = [
        ("Header", {"fields": ['title', 'subtitle', 'game_slug', 'genre','author','image']}),
        ("Content", {"fields": ['content', 'notes']}),
        ("Date", {"fields": ['modified']}),
        ("Price", {"fields": ['price']}),
        ("Video", {"fields": ['video']}),
    ]

# Register your models here.
admin.site.register(Genre, GenreAdmin)
admin.site.register(Game, GameAdmin)
