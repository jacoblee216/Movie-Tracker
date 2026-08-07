from django.core.management.base import BaseCommand
from core.models import Movie

MOVIES = [
    {"name": "Inception", "genres": ["sci-fi", "thriller"]},
    {"name": "Interstellar", "genres": ["sci-fi", "drama"]},
    {"name": "The Dark Knight", "genres": ["action", "thriller", "crime"]},
    {"name": "Dunkirk", "genres": ["war", "action", "drama"]},
    {"name": "The Matrix", "genres": ["sci-fi", "action"]},
    {"name": "Pulp Fiction", "genres": ["crime", "drama"]},
    {"name": "Kill Bill: Vol. 1", "genres": ["action", "crime"]},
    {"name": "Django Unchained", "genres": ["western", "drama"]},
    {"name": "The Grand Budapest Hotel", "genres": ["comedy", "drama"]},
    {"name": "Moonrise Kingdom", "genres": ["comedy", "romance", "drama"]},
    {"name": "Get Out", "genres": ["horror", "thriller"]},
    {"name": "Us", "genres": ["horror", "thriller"]},
    {"name": "Parasite", "genres": ["thriller", "drama", "comedy"]},
    {"name": "Snowpiercer", "genres": ["sci-fi", "action", "thriller"]},
    {"name": "Spirited Away", "genres": ["fantasy", "animation"]},
    {"name": "Princess Mononoke", "genres": ["fantasy", "animation", "action"]},
    {"name": "Mad Max: Fury Road", "genres": ["action", "sci-fi"]},
    {"name": "The Godfather", "genres": ["crime", "drama"]},
    {"name": "Apocalypse Now", "genres": ["war", "drama"]},
    {"name": "Jaws", "genres": ["thriller", "horror"]},
    {"name": "Jurassic Park", "genres": ["sci-fi", "adventure"]},
    {"name": "Schindler's List", "genres": ["war", "drama", "history"]},
    {"name": "Alien", "genres": ["sci-fi", "horror"]},
    {"name": "Blade Runner", "genres": ["sci-fi", "thriller"]},
    {"name": "Gladiator", "genres": ["action", "drama", "history"]},
    {"name": "Fight Club", "genres": ["drama", "thriller"]},
    {"name": "Se7en", "genres": ["crime", "thriller", "horror"]},
    {"name": "The Social Network", "genres": ["drama", "biography"]},
    {"name": "La La Land", "genres": ["romance", "musical", "drama"]},
    {"name": "Whiplash", "genres": ["drama", "music"]},
]

class Command(BaseCommand):
    help = "Seeds the database with 30 starter movies"

    def handle(self, *args, **options):
        Movie.objects.all().delete()
        for m in MOVIES:
            Movie.objects.create(**m)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(MOVIES)} movies."))