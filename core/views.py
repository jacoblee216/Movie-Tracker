from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, UserProfile


def home(request):
    if request.method == "POST":
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        action = request.POST.get("action")
        movie_id = request.POST.get("movie_id")
        if action == "add":
            movie = Movie.objects.filter(id=movie_id).first()
            if (movie):
                profile.movie_list.add(movie)
            return redirect("home")
        elif action == "remove":
            movie = profile.movie_list.get(id=movie_id)
            profile.movie_list.remove(movie_id)
            return redirect("home")
        
    movies = Movie.objects.all()
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    movie_list = profile.movie_list.all()
    unadded_list = []
    
    for movie in movies:
        if movie not in movie_list:
            unadded_list.append(movie)

    favorite_genres = genre_handler(movies, profile)

    context = {
        "unadded_movies": unadded_list,
        "movie_list": movie_list,
        "favorite_genres": favorite_genres,
    }
    return render(request, "home.html", context)

def genre_handler(movies, profile):
    movie_list = profile.movie_list.all()

    favorite_genres = []
    genre_counter = {}
    for movie in movie_list: # counting user's favorite genres
        for genre in movie.genres:
            if genre not in genre_counter:
                genre_counter[genre] = 1
            else:
                genre_counter[genre] += 1
    while genre_counter:
        temp = -1
        name = ""
        for genre, count in genre_counter.items():
            if temp <= count:
                temp = count
                name = genre
        favorite_genres.append(name)
        del genre_counter[name]

    while (len(favorite_genres) > 3): # only return the top 3 genres
        favorite_genres.pop()

    return favorite_genres