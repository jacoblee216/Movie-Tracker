from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, AppUser

"""

GOAL OF PROJECT:
Create an app that prompts users for taste in movies
Calculate their taste and display movies based on taste
Create example user records to create an average user's taste


Potential features and additions:
Integrate a movie api to fetch data on movies
Create visual graph to display average movie taste and compare it to user

"""

def home(request):
    user_id = request.session.get("app_user_id")
    if not user_id:
        return redirect("login")
    user = AppUser.objects.get(id=user_id)
    if request.method == "POST":
        action = request.POST.get("action")
        movie_id = request.POST.get("movie_id")
        if action == "add": 
            movie = Movie.objects.filter(id=movie_id).first()
            if (movie):
                user.movie_list.add(movie)
            return redirect("home")
        elif action == "remove":
            movie = user.movie_list.get(id=movie_id)
            user.movie_list.remove(movie_id)
            return redirect("home")
        
    movies = Movie.objects.all()
    movie_list = user.movie_list.all()
    unadded_list = []
    
    for movie in movies: # iterates through user-liked movies and adds only unliked movies to the master list
        if movie not in movie_list:
            unadded_list.append(movie)

    favorite_genres = genre_handler(user)

    context = { # passes these variables to html file
        "unadded_movies": unadded_list,
        "movie_list": movie_list,
        "favorite_genres": favorite_genres,
        "username": user.username,
    }
    return render(request, "home.html", context)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = AppUser.objects.filter(username=username).first()
        if not user: # case: username not found
            error = f"User not found with username \"{username}\""
            return render(request, "login.html", {"error": error})
        
        if not user.check_password(password): # case: password is incorrect for that user
            error = f"Incorrect password for \"{username}\""
            return render(request, "login.html", {"error": error})
        
        request.session["app_user_id"] = user.id
        return redirect("home")
    return render(request, "login.html")
def register(request):
    print("METHOD: ", request.method)
    if request.method == "POST":
        username = request.POST.get("username")
        first_password = request.POST.get("password1")  # password1 is first password, password2 is confirm password
        confirmed_password = request.POST.get("password2")
        if not username or not first_password or not confirmed_password: # case: empty text field
            return render(request, "register.html", {"error": "Error: Empty Field"})
        
        if AppUser.objects.filter(username=username).exists(): # case: username is taken
            return render(request, "register.html", {"error": f"Username \"{username}\" is already taken"})
        
        if (first_password != confirmed_password): # case: passwords do not match
            return render(request, "register.html", {"error": "Passwords do not match"}) 
        
        user = AppUser(username=username)
        user.set_password(first_password)
        user.save()
        request.session["app_user_id"] = user.id
        return redirect("home")

    return render(request, "register.html")
def genre_handler(user):
    movie_list = user.movie_list.all()

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