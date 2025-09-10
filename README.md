# WordWarriors

#### Description:

WordWarriors (or hangman) is a web-based gaming application designed to help high school graduates prepare their vocabularies for university or college. The game starts by asking users to log in or register. After logging in, users are taken to the main menu, where they can start a new game, load a game, or view their profile.

Starting a new game creates a new session where users must guess the letter or word of the target word for the level. Hints and a category classifying the word (related to academic classes like economics or political science) are provided. Users can select the guess type, either letters or words, with built-in validation functions to handle invalid guesses. Each correct guess earns 10 points, while each wrong guess deducts 10 points and 1 life. Players start with 10 lives per game, and each level features different words, hints, and categories.

Selecting "load game" in the main menu will resume the last game if it isn't over (a game ends when the player runs out of lives). The profile section shows the user's name, an auto-created email label, and a performance dashboard including highest score, highest level, successful guess rates, and a graph displaying the subject with the best performance (in terms of average score per level).

WordWarriors is built using Django for the full stack and backend, with HTML, CSS, and JavaScript for the front end.

### Features:

- **Login/Registration:** Secure user authentication for personalized gameplay.
- **Start New Game:** Begin a new game session with unique words, hints, and categories.
- **Load Game:** Resume the last game session if it hasn't ended.
- **Profile Section:** View personal information and performance statistics.

### Gameplay Mechanics:

- **Guessing:** Choose to guess letters or words, with hints and categories provided.
- **Validation:** Built-in functions to handle invalid guesses.
- **Scoring:** Earn 10 points for each correct guess; lose 10 points and 1 life for each incorrect guess.
- **Lives:** Start each game with 10 lives; game ends when lives run out.
- **Levels:** Different words, hints, and categories for each level.

### Navigation:

- **Main Menu Options:**
  - **Start New Game:** Begin a new game.
  - **Load Game:** Resume the last game session.
  - **Profile:** View personal information and performance statistics.


## Project Base:

Framework : Django 5.2

Database : SQLite


### Installation

Follow these steps to set up and run the Django Poll Application:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/GGurol/wordwarriors.git
   ```

2. Navigate to the project directory:

   ```bash
   cd wordwarriors
   ```

3. Build the docker and build:

   ```bash
   docker compose up --build -d
   ```

4. Apply database migrations:

   ```bash
   docker compose exec web python manage.py makemigrations
   docker compose exec web python manage.py migrate
   ```

5. Create a superuser to access the admin interface:

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```


6. Now, : http://localhost:8000 register and play the game.

