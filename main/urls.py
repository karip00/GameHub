from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("disclaimer", views.disclaimer, name="disclaimer"),
    path("about", views.about, name="about"),
    path("newsletter", views.newsletter, name="newsletter"),
    path("new_genre", views.new_genre, name="genre-create"),
    path("new_post", views.new_post, name="post-create"),
    path("<genre>", views.genre, name="genre"),
    path("<genre>/update", views.genre_update, name="genre_update"),
    path("<genre>/delete", views.genre_delete, name="genre_delete"),
    path("<genre>/<game>", views.game, name="game"),
    path("<genre>/<game>/update", views.game_update, name="game_update"),
    path("<genre>/<game>/delete", views.game_delete, name="game_delete"),
    path("<genre>/<game>/upload_image", views.upload_image, name="upload_image"),
]