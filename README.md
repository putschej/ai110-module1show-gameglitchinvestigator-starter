# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.

It's a number guessing game. The computer picks a secret number and you try to
guess it, and it tells you if you're too high or too low until you get it. The
difficulty setting changes two things: the range of numbers and how many guesses
you get. I suppose this is fun to some people.

- [x] Detail which bugs you found.

A few things were off when I first played it:

- The hints were backwards. If I guessed too high it told me to go higher, which
  sends you the wrong way.
- The "New Game" button didn't really start a new game. It kept the old score and
  history, and if you had already won or lost it wouldn't let you play again.
- The secret number kept changing type. On every other guess the code turned the
  secret into text, so the comparison got weird and the hint was wrong.
- The difficulty range didn't actually apply on a new game. It always picked from
  1 to 100 no matter what I set.
- The difficulty was kind of backwards too. "Normal" uses 1 to 100 with the most
  guesses, but that's a wider range than "Hard" (1 to 50), so Normal is really
  the hardest.

- [x] Explain what fixes you applied.

I picked two to actually fix:

- **Backwards hints.** I moved `check_guess` out of `app.py` into `logic_utils.py`
  and swapped the messages so a too-high guess now says "Go LOWER" and a too-low
  guess says "Go HIGHER."
- **New Game not resetting.** I added a `reset_progress()` function in
  `logic_utils.py` and called it from the New Game button so the score, status,
  and history all clear out. Now a finished game actually lets you start over.

After each fix I ran `pytest` to make sure it worked. I fixed the old tests that
were checking the wrong thing and added new tests for both bugs, and they all pass.

## 📸 Demo Walkthrough

Here's a sample game from start to finish so you can follow along without running it.
I left it on Normal difficulty, and the secret number was 63.

1. I start a new game.
2. The sidebar shows the range is 1 to 100.
3. The sidebar shows I get 8 guesses.
4. I open "Developer Debug Info" and see the secret is 63.
5. I guess 40.
6. The game says "Too Low."
7. It tells me to go HIGHER.
8. I guess 80.
9. The game says "Too High."
10. It tells me to go LOWER.
11. I guess 60.
12. The game says "Too Low," go HIGHER.
13. The attempts-left counter ticks down by one.
14. I guess 63.
15. The game says "Correct!" and throws the balloons.
16. It shows the secret was 63 and my final score.
17. It locks the game so I can't keep guessing.
18. I click New Game.
19. The score, history, and status all reset.
20. It picks a fresh secret number.
21. It lets me play again instead of getting stuck on the "you already won" screen.

## 🧪 Test Results

```
$ python -m pytest tests/ -v
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-9.1.1, pluggy-1.6.0
collected 14 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 14%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 21%]
tests/test_game_logic.py::test_too_high_message_says_go_lower PASSED     [ 28%]
tests/test_game_logic.py::test_too_low_message_says_go_higher PASSED     [ 35%]
tests/test_game_logic.py::test_reset_progress_clears_carryover PASSED    [ 42%]
tests/test_game_logic.py::test_reset_progress_status_allows_restart PASSED [ 50%]
tests/test_game_logic.py::test_reset_progress_history_is_fresh_list PASSED [ 57%]
tests/test_game_logic.py::test_negative_number_is_parsed PASSED          [ 64%]
tests/test_game_logic.py::test_decimal_is_truncated_to_int PASSED        [ 71%]
tests/test_game_logic.py::test_extremely_large_number_is_parsed PASSED   [ 78%]
tests/test_game_logic.py::test_large_guess_reads_as_too_high PASSED      [ 85%]
tests/test_game_logic.py::test_negative_guess_reads_as_too_low PASSED    [ 92%]
tests/test_game_logic.py::test_non_numeric_input_is_rejected_gracefully PASSED [100%]

============================= 14 passed in 0.04s =============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
