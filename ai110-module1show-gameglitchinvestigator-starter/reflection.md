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

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
