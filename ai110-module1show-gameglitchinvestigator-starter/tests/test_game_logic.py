from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_check_guess_integer_secret_even_attempt():
    # Regression: secret must stay an integer on even attempts (not str-converted).
    # guess=30 < secret=42 should return "Too Low", not raise TypeError or miscompare.
    outcome, _ = check_guess(30, 42)
    assert outcome == "Too Low"

def test_hint_message_direction():
    # Regression: hint messages were swapped — verify correct direction.
    _, msg_high = check_guess(60, 50)
    assert "LOWER" in msg_high

    _, msg_low = check_guess(40, 50)
    assert "HIGHER" in msg_low
