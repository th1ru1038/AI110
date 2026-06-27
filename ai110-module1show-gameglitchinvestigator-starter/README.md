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

- [x] **Game purpose:** A Streamlit number-guessing game where the player tries to guess a secret number within a limited number of attempts, receiving "too high" / "too low" hints after each guess.

- [x] **Bugs found:**
  1. On even-numbered attempts, the secret number was converted to a string before being compared to the guess, causing a type mismatch that triggered an incorrect fallback comparison (string comparison instead of numeric).
  2. The hint *messages* were swapped — a "Too High" outcome displayed "Go HIGHER!" instead of "Go LOWER!", and vice versa, even though the underlying outcome label was correct.
  3. (Identified but not fixed, documented in reflection.md) The attempts counter initializes at 1 instead of 0, causing the display to start at 7 instead of 8. The "New Game" button also fails to reset score and guess history.
  
- [x] **Fixes applied:**
  1. Removed the even/odd string-conversion logic so the secret number always stays an integer, eliminating the broken fallback path entirely.
  2. Swapped the hint message strings so "Too High" correctly says "Go LOWER!" and "Too Low" correctly says "Go HIGHER!"
  3. Refactored `check_guess` out of `app.py` into `logic_utils.py`, replacing the original stub, and updated `app.py` to import it.


## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User enters a guess of 40 against a secret of 50 → game returns "Too Low" with the message "Go HIGHER!"
2. User enters a guess of 70 → game returns "Too High" with the message "Go LOWER!"
3. Score updates correctly after each guess based on the outcome
4. User enters a guess of 50 → game returns "Win" and displays a success message
5. Guess history updates to reflect each submitted guess in order

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
