from django.urls import path
from . import views


urlpatterns = [
    # defaults
    path('', views.index, name="index"),

    # Access Routes
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),

    # Performance Routes
    path('profile', views.profile, name="profile"),
    path('chart', views.chart, name="chart"),

    # Setup Routes
    path('populate', views.populate, name="populate"),

    # Game Routes
    path('game/new=<int:new>', views.game, name="game"),
    path('guess/game_id=<int:game_id>', views.guess, name="guess"),

]
