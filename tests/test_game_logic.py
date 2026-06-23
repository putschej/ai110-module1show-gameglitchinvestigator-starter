from logic_utils import check_guess, reset_progress, parse_guess

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

# FIX: the regression tests below were written with Claude in agent mode
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

# CHALLENGE 1: edge-case input handling. These check that parse_guess (and
# check_guess) handle unusual inputs gracefully instead of crashing.
def test_negative_number_is_parsed():
    # Edge case: a minus sign is valid int syntax, so a negative guess should
    # parse cleanly rather than error out.
    ok, value, err = parse_guess("-7")
    assert ok is True
    assert value == -7
    assert err is None

def test_decimal_is_truncated_to_int():
    # Edge case: a player might type a decimal; parse_guess should coerce it to
    # an int (truncating toward zero) instead of failing.
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None

def test_extremely_large_number_is_parsed():
    # Edge case: Python ints are arbitrary precision, so a huge value should
    # parse without overflowing or crashing.
    big = "100000000000000000000"
    ok, value, err = parse_guess(big)
    assert ok is True
    assert value == int(big)
    assert err is None

def test_large_guess_reads_as_too_high():
    # A very large guess must still be classified correctly by check_guess.
    outcome, _ = check_guess(10 ** 18, 50)
    assert outcome == "Too High"

def test_negative_guess_reads_as_too_low():
    # A negative guess must still be classified correctly by check_guess.
    outcome, _ = check_guess(-7, 50)
    assert outcome == "Too Low"

def test_non_numeric_input_is_rejected_gracefully():
    # Edge case: garbage text should be rejected with a friendly message, not
    # an unhandled exception.
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."
