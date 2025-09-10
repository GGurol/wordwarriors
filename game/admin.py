# game/admin.py

from django.contrib import admin
from .models import User, Game # NOTE: Import your model names here

# This tells Django to show the User and Game models in the admin panel
admin.site.register(User)
admin.site.register(Game)