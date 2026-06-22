from logic_utils import check_guess, reset_progress

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    # FIXED: check_guess returns a (outcome, message) tuple, so assert on the
    # outcome element instead of comparing the whole tuple to a bare string.
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    # FIXED: unpack the (outcome, message) tuple and check the outcome label.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    # FIXED: unpack the (outcome, message) tuple and check the outcome label.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# FIX: COLLAB: the regression tests below were written with Claude in agent mode
# — it proposed asserting on the hint message and the reset fields, then ran
# pytest to confirm each fix; I reviewed the assertions for correctness.
def test_too_high_message_says_go_lower():
    # BUG 1 regression test: a guess that is too high must tell the player to
    # go LOWER (the original bug said "Go HIGHER", pointing the wrong way).
    _, message = check_guess(60, 50)
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_too_low_message_says_go_higher():
    # BUG 1 regression test: a guess that is too low must tell the player to
    # go HIGHER (the original bug said "Go LOWER", pointing the wrong way).
    _, message = check_guess(40, 50)
    assert "HIGHER" in message
    assert "LOWER" not in message

def test_reset_progress_clears_carryover():
    # BUG 2 regression test: a new game must zero the score, set status back to
    # "playing", and empty the history so no old game state carries over.
    state = reset_progress()
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []

def test_reset_progress_status_allows_restart():
    # BUG 2 regression test: status must return to "playing" specifically (not
    # stay "won"/"lost"), which is what lets a finished game be restarted.
    assert reset_progress()["status"] == "playing"

def test_reset_progress_history_is_fresh_list():
    # BUG 2 regression test: each reset must hand back its own empty list, so
    # mutating one game's history can never leak into the next game.
    first = reset_progress()
    first["history"].append("stale")
    assert reset_progress()["history"] == []
