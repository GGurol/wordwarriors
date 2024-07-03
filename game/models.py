from django.db import models
from django.contrib.auth.models import AbstractUser


# user authentication
class User(AbstractUser):
    pass


# in-game mechanics
class Word(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    text = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.text} in {self.category} category"


class Hint(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    text = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class Level(models.Model):
    level = models.IntegerField(primary_key=True, auto_created=True)
    word_id = models.ForeignKey("Word", on_delete=models.CASCADE)
    hint_id = models.ForeignKey("Hint", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.level}: Word {self.word_id} and Hint ID of {self.hint_id}"


# levelling
class Game(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, default=1)
    total_game_score = models.IntegerField(default=100)
    last_level = models.IntegerField(default=1)
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    lives_left = models.IntegerField(default=10)

    def __str__(self):
        return f"Last Level of {self.last_level} with {self.lives_left} Lives Left"


class GameLevel(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    level = models.ForeignKey("Level", on_delete=models.CASCADE)
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    level_game_score = models.IntegerField(default=100)
    guessed_strings = models.CharField(
        max_length=25, default=" .", null=True, blank=True)
    win = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.level} Only '{self.guessed_strings}' guessed"


# playing
TYPES = [("Letter", "Word")]


class Guess(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    type = models.CharField(max_length=50, choices=TYPES, blank=True)
    text = models.CharField(max_length=100, blank=True, null=True)
    game_level_id = models.ForeignKey("GameLevel", on_delete=models.CASCADE)
    guess_datetime = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField(null=True, blank=True)

    def __str__(self):
        achieve = "Right" if self.result > 0 else "Wrong"
        return f"{achieve} {self.type} guess of '{self.text}' made on {self.guess_datetime}"
