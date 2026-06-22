def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: COLLAB: refactored this function out of app.py into logic_utils.py
    # using Claude in agent mode, which also caught and fixed the backwards hint.
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # BUG 1 FIX: hint direction now matches the outcome — if the guess is
        # too high the player should go LOWER, and if too low they go HIGHER.
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def reset_progress():
    """
    Return the progress fields a new game must clear.

    FIX: COLLAB: Claude (agent mode) suggested extracting the New Game reset
    into this small pure function so the fix could be unit-tested; I reviewed it
    and wired it into app.py.

    BUG 2 lived in the New Game handler: it reset attempts and secret but left
    score, status, and history untouched, so old results carried over and a
    finished game (status "won"/"lost") could never be restarted. Returning
    these as a fresh dict makes the reset explicit and unit-testable.
    """
    return {"score": 0, "status": "playing", "history": []}
