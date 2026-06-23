# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
Looks like a web form input on my browser.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
The hints are going the wrong direction.
New Game button does not work, it's keeping the history from previous games.
The first click on submit does not register.
Settings: easy and hard do not update the actual range on the game.
Normal setting is 1-100 range but that should be hardest.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 70 when secret is 50 | Hint should say "Too High" and tell me to go lower | Hint says "Too High" but message is "📈 Go HIGHER!" | None |
| Click New Game after a finished game | Game state resets: history cleared, attempts reset, and new secret generated for current difficulty | History and score stay from previous game; new game does not fully reset state | None |
| Select Hard difficulty and start a new game | Secret range should be 1 to 50 and hint text should reflect that range | Secret is still generated from 1 to 100 and sidebar range text is inconsistent | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
At first, I used an AI called raptor because I didn't understand the side panel in VS Code.  Then I switched it to Claude.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I asked Claude to check my list of bugs against the actual codebase. It confirmed the backwards hints in `check_guess` and pointed out two bugs I had missed: the `attempts % 2 == 0` line that turns the secret into a string on even guesses (causing wrong hints intermittently) and the New Game button never resetting `status`/`history`. I verified these by reading the lines it cited in `app.py` and by reproducing the even-guess bug in the running game, so I trusted them only after seeing the behavior and the code myself.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
The most misleading AI output was the game's own AI-generated code, which the caption confidently presents as "production-ready" — an implicit suggestion that the code already works as written. That was incorrect: when I ran the game the hints sent me the wrong direction, and reading `app.py` showed the New Game button never reset `score`, `status`, or `history`, so finished games stayed stuck. I verified the claim was false two ways — by playing the game and watching the wrong hints, and by reading the code and writing pytest tests that the original version would have failed (for example asserting a too-high guess says "LOWER"). My takeaway: a confident tone from AI is not evidence the code is correct, so I verify every suggestion against the code and the running app.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Claude and I used two signals instead of just trusting the screen. First, I made sure I could explain *why* the code was wrong: for the hint bug the outcome label ("Too High") was correct and only the message ("Go HIGHER!") pointed the wrong way, so the fix was swapping the messages. Second, I wrote a test that fails on the old code and passes on the new — `test_too_high_message_says_go_lower` would have failed against the original "Go HIGHER!". A bug only counted as fixed once I could both explain the cause and back it with a passing test.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
Claude and I ran `python -m pytest tests/test_game_logic.py -v` and ended with 8 passing tests. The most useful was the first run: `test_winning_guess` asserted `check_guess(50, 50) == "Win"`, but the function returns a tuple `("Win", "🎉 Correct!")`, so the test and the code disagreed on the function's contract. That showed me my code wasn't returning what the test expected, and I fixed it by unpacking the tuple (`outcome, message = check_guess(...)`).

- Did AI help you design or understand any tests? How?
Yes. Claude pointed out that the original tests only checked the outcome label ("Too High"), which was never broken, instead of the message text where the hint bug actually lived — so the starter tests gave false confidence. It then proposed the regression assertions (like `"LOWER" in message` and `"HIGHER" not in message`) and ran pytest to confirm each fix. I reviewed every assertion before keeping it, which fit the suggestion from Question 2 that confident AI output still has to be verified.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit re-runs your entire script from top to bottom every time the user interacts with the app — clicking a button, typing in a field, or toggling a control all trigger a full rerun. Because of that, ordinary local variables don't persist; they get recreated on every rerun, which is why the secret number kept getting re-generated on each click. Session state (`st.session_state`) is the fix: it's a dictionary that persists across reruns, so values you store in it (the secret, score, attempts, history) survive instead of being reset. The New Game bug we fixed was a session state bug — it only reset some of the stored keys and left the old score and history in place.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
I liked dropping `# BUG 1` and `# BUG 2` comments right in the code at the spots that were broken. It made it easy to find those places again later, and it gave me a quick way to point Claude straight at a specific line when we talked instead of re-describing the same bug over and over. I want to keep using little markers like that as a way to organize my own work and to communicate with AI.

- What is one thing you would do differently next time you work with AI on a coding task?
Next time I'd modularize my fixes more from the start — break the changes into smaller, separate pieces instead of fixing things in one big chunk. On this project we ended up pulling functions out into `logic_utils.py` so they could be tested, and doing that kind of split earlier would have kept things cleaner and easier to test as I went.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
Honestly, this didn't change how I think about AI-generated code very much. I already assumed AI output needs to be checked, and this mostly confirmed it — a confident "production-ready" label doesn't mean the code actually works.
