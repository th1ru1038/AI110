# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  - Sometimes, the number of attempts went to negatives. I expected the attempts to be 0 when it's over, and restart when we click on New Game button.

  - Any number chosen below the actual number, tells us that we should choose an even lower number, whereas it should be a higher number

  - Any number chose above the actual number, tells us that we should choose an even higher number, whereas it should be a lower number

  - When you first open the page, the number of attempts left begin with 7, where it mentions the user has attempted once already, whereas that isn't the case and nothing has been attempted. It is only when we click on "new game" button, the number of attempts restarts to 8, with the score remaining unchanged, and the history no being cleared. Also, if the number of attempts ran out, then it doesn't allow the user to submit a number regardless, so the number of attempts never reduces post that.
  
  - When clicking on submit guess, the first time it's not showing up on history despite the number of attempts reducing. It only shows up on th esceond time clicking on it, but th enumber of attempts reduced again.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 57 | Go lower (as the secret is 44) | Go higher | |
| Clicked New Game | Restart the attempts to 7| Restarted to 8| |
| 43 | Go higher| Go lower | |


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude (Claude Code in VS Code) for this project.

**Correct example:** I had logged a bug where guessing below the secret number told me to go higher, and guessing above it told me to go lower, the hints seemed backwards. I asked Claude to find the cause. It correctly identified two separate bugs hiding behind the same symptom: 
  1) On even-numbered attempts, app.py converted the secret number to a string before comparing it, which triggered a TypeError fallback that did string comparison instead of numeric comparison, and 
  
  2) In the normal comparison branch, the outcome label was correct but the hint message text itself was swapped (ex, a "Too High" result displayed "Go HIGHER!" instead of "Go LOWER!"). I verified this was correct by writing pytest tests that checked specific guess/secret pairs against the expected hint direction, running them and confirming they passed, and then manually playing the game to confirm the hints made sense.

**Incorrect/misleading example:** I asked Claude to investigate why the attempts counter could go negative. It gave a detailed explanation claiming that a user could click "Submit" multiple times before Streamlit finished rerunning the script, causing the attempts counter to increment past the limit, which was described as a kind of race condition. This sounded plausible but I pushed back and asked it to walk me through exactly how that would happen given that Streamlit reruns the whole script on every interaction. When pressed, Claude admitted the race condition it described doesn't actually exist in Streamlit's synchronous execution model. Every click triggers exactly one full rerun, so there's no way for clicks to queue up. It revised its explanation to say the "negative attempts" report was more likely a misread of a separate, simpler bug (the counter initializing at 1 instead of 0). This taught me that a confident, technically-detailed explanation isn't automatically a correct one — I had to specifically ask "is this mechanism actually possible" before it caught its own mistake.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I considered a bug "really fixed" only once two things were true: a pytest test specifically targeting that bug passed, and I could no longer reproduce the original symptom by manually playing the game.

For the stringification bug, I wrote a pytest test that called check_guess with an integer secret and confirmed it returned the correct outcome (rather than triggering the old string-comparison fallback). For the swapped-hint-message bug, I wrote a test that checked the message text contained "LOWER" or "HIGHER" matching the correct direction for a given guess/secret pair. Both tests passed, and I then ran the app live with streamlit run app.py and confirmed both hint direction and the underlying logic worked correctly during actual gameplay.

AI helped design both tests, where I described what behavior I wanted verified (the specific guess/secret scenario), and Claude wrote the test function and assertions. I reviewed each diff before running it to make sure the test was actually checking what I intended, not just checking that the code ran without error.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit doesn't work like a normal app where you click something and only that one part of the screen updates. Every time you interact with anything such as clicking a button, typing in a box, Streamlit reruns your *entire* script from top to bottom, and whatever you saved in st.session_state is the only thing that survives between those reruns. Everything else gets recalculated fresh each time.

This explains a lot of subtle bugs: if something is supposed to update based on an action you just took, but the code that *displays* it runs earlier in the script than the code that *changes* it, you won't see the update until the next rerun (the next click) which looks like a one-click delay, even though nothing is "broken" in the traditional sense. It's less about a wrong calculation and more about *when* in the script's top-to-bottom run something happens relative to when it's displayed.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep: asking the AI to explain its own reasoning when something it says sounds too confident or too neat, especially for a tricky mechanism (like Streamlit's rerun model). Pushing back with "walk me through exactly how that happens" caught a wrong explanation that I would have otherwise accepted at face value.

One thing I'd do differently next time: describe bugs to the AI by symptom only, without sharing my own hypothesis about the cause, at least once before steering it — that gave me a more honest read on whether its diagnosis was actually independently correct, versus just agreeing with what I already suspected.

This project changed how I think about AI-generated code mainly by showing me that a clear, well-structured explanation isn't the same as a correct one — I have to verify claims about how the underlying system actually behaves (in this case, Streamlit's execution model) rather than just checking whether the proposed fix resolves the symptom on the surface.
