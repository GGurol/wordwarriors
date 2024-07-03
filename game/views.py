import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
from game.models import *

per_score = 10


#  Main Menu Views
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, "game/index.html")


#  Authentication Views
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "game/login.html", {
                    "message": "Invalid username and/or password."
                })
        else:
            return render(request, "game/login.html", {
                "message": "Username and password are required."
            })
    else:
        return render(request, "game/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm-password"]
        if password != confirmation:
            return render(request, "game/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password)
            user.set_password(password)
            user.save()
        except IntegrityError:
            return render(request, "game/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "game/register.html")


# Game Views
def game(request, new):

    # load last game or create a new game
    last_game = 0 if Game.objects.all().last() == None else Game.objects.all().last().id
    if new == 1:
        game = Game.objects.create(
            last_level=1, user_id=request.user, id=last_game+1)
        game_session = GameLevel.objects.create(
            game_id=game, level=Level.objects.filter(level=1).first())

    # fetch the game and level data
    game = Game.objects.filter(user_id=request.user).last()
    game_level = Level.objects.filter(level=game.last_level).first()
    game_session = GameLevel.objects.filter(
        game_id=game, level=game_level).first()
    if game_session is None:
        game_session = GameLevel.objects.create(
            game_id=game, level=Level.objects.filter(level=game.last_level).first())
    game_word = Word.objects.filter(id=game_level.word_id.id).first()
    game_hint = Hint.objects.filter(id=game_level.hint_id.id).first()
    game_char = decrypt(game_word.text, game_session.guessed_strings)

    return render(request, "game/game.html", {
        "level": game_level.level,
        "word": game_word.text,
        "char": game_char,
        "category": game_word.category,
        "hint": game_hint.text,
        "game_id": game.id,
        "life":  game.lives_left,
        "score": game.total_game_score,
        "guess": {
            "guessed": False,
        }
    })


def guess(request, game_id):

    # retreive the necessary game data
    game = Game.objects.filter(id=game_id).first()
    game_level = Level.objects.filter(level=game.last_level).first()
    game_session = GameLevel.objects.filter(
        game_id=game_id, level=game_level).first()
    game_word = Word.objects.filter(id=game_level.word_id.id).first()
    word = game_word.text.lower()

    # get the current game chars
    game_char, char_array = decrypt(
        game_word.text, game_session.guessed_strings, both=True)

    message = ""

    if request.method == "POST":

        # work on the guess
        data = json.loads(request.body)
        guess = data['guess'].lower()
        type = data['type'].lower()
        extra_points, stream_word = 0, []
        if (type == "letter" and guess in game_char.lower()):
            message = "You already have guessed this letter."
            color = "#FDDA0D"

        elif (type == "letter" and guess in word):
            game.total_game_score += per_score
            game_session.level_game_score += per_score

            # add the guess to the guessed strings
            game_session.guessed_strings += guess + "."
            game.save(), game_session.save()
            message = "Congratulations! Your guess is correct."
            color = "green"
            result = 1

        elif (type == "word" and guess == word):

            for i in range(len(word)):
                if char_array[i] == " _":
                    stream_word.append(word[i])

            extra_points += per_score*len(list(set(stream_word)))
            game.total_game_score += extra_points
            game_session.level_game_score += extra_points

            # add the guess to the guessed strings
            game_session.guessed_strings += guess + "."
            game.save(), game_session.save()
            message = "Congratulations! Your guess is correct."
            color = "green"
            result = len(list(set(stream_word)))

        else:
            game.lives_left -= 1
            if game.total_game_score > 0:
                game.total_game_score -= per_score
            game_session.level_game_score -= per_score
            game.save(), game_session.save()
            message = "Sorry, your guess is incorrect. Please try again."
            color = "red"
            result = -1

        # repopulate the characters to be guessed
        game_char = decrypt(game_word.text, game_session.guessed_strings)
        if "_" not in game_char:
            game.last_level += 1
            game_session.win = True
            game.save()

        game_over = False
        if game.lives_left <= 0:
            game_over = True

        guess = Guess.objects.create(
            type=type, text=guess, game_level_id=game_session, result=result)

        return JsonResponse({
            "game_over": game_over,
            "game_char": game_char,
            "guessed": True,
            "color": color,
            "message":  message,
        })

    return redirect('game', level=game_level.level, new=0)


def decrypt(word, strings, both=False):

    # generate decrypted guessed characters
    char_array = [" _"] * len(word)
    guessed_chars = [item for item in strings.split(".")]

    for char in guessed_chars:
        for i in range(len(word)):
            if word.lower() == char.lower():
                char_array = [letter for letter in word]

            elif word[i].lower() == char.lower():
                char_array[i] = char.upper()

    game_char = ""
    for char in char_array:
        game_char += " " + char

    if both:
        return game_char, char_array

    return game_char


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        games = Game.objects.filter(user_id=request.user)
        user = request.user.username

        # scores and levels
        all_scores, all_levels, guesses = [], [], []
        for game in games:
            for game_level in GameLevel.objects.filter(game_id=game):
                items = [guess.result for guess in Guess.objects.filter(
                    game_level_id=game_level)]
                if len(items) > 0:
                    for item in items:
                        guesses.append(item)

            score, level = game.total_game_score, game.last_level
            all_scores.append(score), all_levels.append(level)

        try:
            right_guess, wrong_guess = 0, 0
            for guess in guesses:
                if guess > 0:
                    right_guess += guess
                else:
                    wrong_guess += -guess
            guess_rate = int((right_guess / (wrong_guess + right_guess))*100)
        except ZeroDivisionError:
            guess_rate = 0

        context = {
            "user": user,
            "best_score": 0 if len(all_scores) == 0 else max(all_scores),
            "highest_level":  0 if len(all_levels) == 0 else max(all_levels),
            "guess_rate": f"{guess_rate}%"
        }
        return render(request, "game/profile.html", {
            "profile": context
        })


def chart(request):
    try:
        games = Game.objects.filter(user_id=request.user)
        scores, raw = [], []

        # check
        for game in games:
            sessions = GameLevel.objects.filter(game_id=game)
            for session in sessions:
                match = re.search(
                    r"Word (.*?) in (.*?) category and Hint ID of (\d+)", str(session.level))
                if match:
                    word, category, hint_id = match.groups()
                    raw.append(
                        {"Subject": category, "Score": session.level_game_score})

            summary = {}
            for item in raw:
                subject = item['Subject']
                score = item['Score']
                if subject not in summary:
                    summary[subject] = {'count': 0, 'total_score': 0}
                    summary[subject]['count'] += 1
                    summary[subject]['total_score'] += score

                # Calculate average score for each subject
                for subject, info in summary.items():
                    summary[subject]['average_score'] = info['total_score'] / \
                        info['count']

        for subject, info in summary.items():
            scores.append({
                'Subject': subject,
                'Score': info['average_score']
            })

        scores.sort(key=lambda x: x['Score'], reverse=True)
    except Exception:
        scores = [{"Subject": "", "Scores": 0}]
        pass
    return JsonResponse({'chartData': scores})


# Setup Views
def populate(request):
    import json
    data_path = "game/data/words.json"

    with open(data_path, 'r') as f:
        words_data = json.load(f)

        for word_data in words_data:
            # check word and create if not exists
            word, _word = Word.objects.get_or_create(
                text=word_data['word'], category=word_data['category'])

            # check hint and create if not exists
            hint, _hint = Hint.objects.get_or_create(text=word_data['hint'])

            # if not exists create level and only if both word and hint were created successfully
            if hint and word and hint.id != None and word.id != None:
                if not Level.objects.filter(word_id=word, hint_id=hint).first():
                    level = Level.objects.create(
                        word_id=word, hint_id=hint)

        # check the word_data
        print(json.dumps(word_data, indent=4))

    return redirect('index')
