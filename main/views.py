from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from .decorators import user_is_superuser
from django.contrib import messages
from django.core.mail import EmailMessage

from .forms import NewsletterForm, GenreCreateForm, GameCreateForm, GenreUpdateForm, GameUpdateForm
from users.models import SubscribedUsers

from .models import Game, Genre
import os
from uuid import uuid4

# Create your views here.
def homepage(request):
    matching_genre = Genre.objects.all()
    
    return render(
        request=request,
        template_name='main/home.html',
        context={"objects": matching_genre}
        )

def disclaimer(request):
    return render(
        request=request,
        template_name='main/disclaimer.html'
        )

def about(request):
    return render(
        request=request,
        template_name='main/about.html'
        )

def genre(request, genre: str):
    matching_genre = Game.objects.filter(genre__slug=genre).all()
    
    return render(
        request=request,
        template_name='main/home.html',
        context={"objects": matching_genre}
        )

def game(request, genre: str, game: str):
    matching_game = Game.objects.filter(genre__slug=genre, game_slug=game, video__startswith='https://www.youtube.com/' ).first()
    
    return render(
        request=request,
        template_name='main/game.html',
        context={"object": matching_game, "video": matching_game.video}
        )

@user_is_superuser
def new_genre(request):
    if request.method == "POST":
        form = GenreCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("homepage")

    else:
         form = GenreCreateForm()

    return render(
        request=request,
        template_name='main/new_record.html',
        context={
            "object": "Genre",
            "form": form
            }
        )

@user_is_superuser
def new_post(request):
    if request.method == "POST":
        form = GameCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f"{form.cleaned_data['genre'].slug}/{form.cleaned_data.get('game_slug')}")

    else:
         form = GameCreateForm()

    return render(
        request=request,
        template_name='main/new_record.html',
        context={
            "object": "Game",
            "form": form
            }
        )

@user_is_superuser
def genre_update(request, genre):
    matching_genre = Genre.objects.filter(slug=genre).first()

    if request.method == "POST":
        form = GenreUpdateForm(request.POST, request.FILES, instance=matching_genre)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    
    else:
        form = GenreUpdateForm(instance=matching_genre)

        return render(
            request=request,
            template_name='main/new_record.html',
            context={
                "object": "Genre",
                "form": form
                }
            )

@user_is_superuser
def genre_delete(request, genre):
    matching_genre = Genre.objects.filter(slug=genre).first()

    if request.method == "POST":
        matching_genre.delete()
        return redirect('/')
    else:
        return render(
            request=request,
            template_name='main/confirm_delete.html',
            context={
                "object": matching_genre,
                "type": "Genre"
                }
            )

@user_is_superuser
def game_update(request, genre, game):
    matching_game = Game.objects.filter(genre__slug=genre, game_slug=game).first()

    if request.method == "POST":
        form = GameUpdateForm(request.POST, request.FILES, instance=matching_game)
        if form.is_valid():
            form.save()
            return redirect(f'/{matching_game.slug}')
    
    else:
        form = GameUpdateForm(instance=matching_game)

        return render(
            request=request,
            template_name='main/new_record.html',
            context={
                "object": "Game",
                "form": form
                }
            )

@user_is_superuser
def game_delete(request, genre, game):
    matching_game = Game.objects.filter(genre__slug=genre, game_slug=game).first()

    if request.method == "POST":
        matching_game.delete()
        return redirect('/')
    else:
        return render(
            request=request,
            template_name='main/confirm_delete.html',
            context={
                "object": matching_game,
                "type": "Game"
                }
            )

@csrf_exempt
@user_is_superuser
def upload_image(request, genre: str=None, game: str=None):
    if request.method != "POST":
        return JsonResponse({'Error Message': "Wrong request"})

    matching_game = Game.objects.filter(genre__slug=genre, game_slug=game).first()
    if not matching_game:
        return JsonResponse({'Error Message': f"Wrong genre ({genre}) or game ({game})"})

    file_obj = request.FILES['file']
    file_name_suffix = file_obj.name.split(".")[-1]
    if file_name_suffix not in ["jpg", "png", "gif", "jpeg"]:
        return JsonResponse({"Error Message": f"Wrong file suffix ({file_name_suffix}), supported are .jpg, .png, .gif, .jpeg"})

    file_path = os.path.join(settings.MEDIA_ROOT, 'GameGenre', matching_game.slug, file_obj.name)

    if os.path.exists(file_path):
        file_obj.name = str(uuid4()) + '.' + file_name_suffix
        file_path = os.path.join(settings.MEDIA_ROOT, 'GameGenre', matching_game.slug, file_obj.name)

    with open(file_path, 'wb+') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': os.path.join(settings.MEDIA_URL, 'GameGenre', matching_game.slug, file_obj.name)
        })

@user_is_superuser
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers').split(',')
            email_message = form.cleaned_data.get('message')

            mail = EmailMessage(subject, email_message, f"GameHub <{request.user.email}>", bcc=receivers)
            mail.content_subtype = 'html'

            if mail.send():
                messages.success(request, "Email sent succesfully")
            else:
                messages.error(request, "There was an error sending email")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

        return redirect('/')

    form = NewsletterForm()
    form.fields['receivers'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
    return render(request=request, template_name='main/newsletter.html', context={'form': form})