# PawPal+ Project Reflection

## 1. System Design

*** Three Core Actions that the User can Perform:  ***

1) Track certain pet care tasks (that are routines)
2) Log in any constraints that can come between your tasks (like integrating your calendar)
3) View today's tasks.

**a. Initial design**

My initial UML has five classes, split between simple data holders and behavior-driven classes:

- **Owner** — represents the pet owner. Holds a `name`, a `preferences` dict (things like preferred start time or available time budget), and a list of `Pet`s they own. Responsible for storing owner-level constraints and owning the pets/tasks — tasks are *for* a pet, but *performed by* the owner, so `Owner` also has a direct relationship to `Task`.
- **Pet** — represents one pet (name, species, breed, age) and holds its own list of `Task`s. Responsible for knowing which tasks belong to it, since one owner can have multiple pets with different care needs.
- **Task** — one unit of pet care (name, duration, priority, category, recurrence, optional preferred time). Responsible for describing what needs to happen and being comparable/checkable against other tasks (e.g., `conflicts_with`).
- **Scheduler** — the engine. Takes a pet's tasks and a time budget/constraints, and is responsible for sorting by priority, filtering out tasks that don't fit the time budget, resolving time-slot conflicts, and producing a `Schedule`.
- **Schedule** — the output of the `Scheduler`: which tasks got scheduled (and when), how much time was used, and which tasks were skipped. Responsible for presenting the plan and explaining the reasoning behind it.

I split `Scheduler` and `Schedule` into separate classes so the scheduling *logic* is testable independently from the *data structure* that holds a finished plan.

**b. Design changes**

I asked my AI assistant to review `pawpal_system.py` against the UML and flag any missing relationships or logic bottlenecks. It found three issues, and I made the following changes:

1. **Added `Owner.all_tasks()`.** The UML said `Owner performs Task`, but the code had no way to actually reach an owner's tasks — you'd have had to manually loop through `owner.pets[i].tasks` yourself. Added a method that aggregates tasks across all of an owner's pets so that relationship is real in code, not just implied on the diagram.
2. **Removed the redundant `tasks` parameter from `Scheduler.generate_plan`.** It originally took `(pet, tasks, available_minutes)`, but `pet` already carries `pet.tasks`. Passing a separate `tasks` list created a bug risk: the two lists could silently disagree about what the pet's tasks actually are. Now `generate_plan` takes `(pet, available_minutes)` and reads tasks directly from `pet.tasks`.
3. **Changed `Schedule.scheduled_tasks` from `list[Task]` to `list[tuple[str, Task]]`.** `add_task(task, time_slot)` accepted a `time_slot`, but the original list type had nowhere to store it — once a task was added, its scheduled time would be lost. Storing `(time_slot, task)` pairs keeps that information available for display/explanation later.

Updated `diagrams/uml.mmd` to match all three changes so the diagram stays accurate to the implementation.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three constraints: task `priority` (high/medium/low), `duration_minutes` against the owner's `available_minutes` budget, and `preferred_time` (used only to detect same-time conflicts, not full overlap). Priority mattered most because the scenario is about a busy owner who needs the most important care (feeding, meds) to happen even if lower-priority tasks (enrichment, grooming) get dropped — so `sort_tasks` sorts by priority first, then by shorter duration as a tiebreaker so more tasks fit in a tight budget.

**b. Tradeoffs**

`Scheduler.resolve_conflicts` only checks for an *exact* `preferred_time` string match (e.g. two tasks both at `"08:00"`) — it does not check whether task durations actually overlap in time (e.g. an 08:00–08:30 walk and an 08:15 feeding). This is reasonable for this scenario because it keeps the conflict logic simple and fast (`O(n)` with a `set`), and most pet care tasks (meds, feeding) are effectively instantaneous relative to the day, so exact-time collisions are the common case worth catching. The cost is that overlapping-duration conflicts (like the walk/feeding example above) currently go undetected — `detect_conflicts` would need to compare time ranges, not just exact strings, to catch that.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI across the whole pipeline: brainstorming the initial class list and responsibilities before any code existed, translating the UML into Python skeletons, implementing scheduling logic incrementally (sorting, filtering, conflict detection, recurrence), writing the test suite, and wiring the Streamlit UI to the logic layer. The most helpful prompts were narrow and concrete rather than open-ended — e.g. "review pawpal_system.py and flag missing relationships or logic bottlenecks" produced specific, actionable findings (three real issues), whereas vague prompts would have produced generic advice. Asking "why" questions about my own design decisions (e.g. why `Pet` holds tasks instead of `Owner`) was also useful for stress-testing the model before locking it into code.

**b. Judgment and verification**

One clear moment: I pushed back when the assistant's first design put tasks directly on `Owner` instead of `Pet`. I pointed out that pet care tasks are inherently pet-specific (a walk is for a specific dog, not the owner in the abstract), even though the owner is the one who performs them. Rather than just picking one, we kept both relationships — `Pet has Task` (ownership) and `Owner performs Task` (who acts on it) — which is reflected in `Owner.all_tasks()`. I verified this wasn't just cosmetic by checking that `all_tasks()` actually aggregates through `pet.tasks` rather than duplicating data, and by writing a test (`test_owner_filter_tasks_by_pet_and_status`) that would fail if the aggregation logic were wrong.

---

## 4. Testing and Verification

**a. What you tested**

The 12-test suite in `tests/test_pawpal.py` covers: object basics (`mark_complete`, `add_task`), sorting correctness (both priority-based and time-based), filtering (time-budget cutoff, and pet/status filtering), conflict detection (both the positive and negative case), recurrence (daily task creates a next occurrence one day later; one-off tasks don't recur), and two edge cases (a pet with zero tasks, and a low-priority task losing a time conflict to a higher-priority one). These mattered because they're exactly the behaviors a busy pet owner would notice if they were wrong — a scheduler that silently drops the wrong task, or "forgets" to warn about a double-booking, would be actively unhelpful rather than just incomplete.

**b. Confidence**

I'd rate my confidence at 4/5. The core sorting/filtering/conflict/recurrence logic is tested and passing, and I manually verified `app.py` boots and the UI flow works end-to-end. What I'd test next with more time: overlapping-duration conflicts (right now `detect_conflicts` only catches exact `preferred_time` matches — see 2b), scheduling across multiple pets in a single combined run rather than one pet at a time, and weekly-recurrence math specifically (only daily recurrence has a dedicated test for the `timedelta` math).

---

## 5. Reflection

**a. What went well**

I'm most satisfied with how the UML-first process paid off — because the classes and their responsibilities were settled before any Python was written, implementing the scheduling logic in Phase 4 was mostly filling in behavior for structure that already made sense, rather than discovering mid-implementation that the class boundaries were wrong.

**b. What you would improve**

I'd redesign conflict detection to compare actual time ranges (start + duration) instead of exact `preferred_time` string matches. The current approach is a known, documented tradeoff (see 2b), but it's the biggest gap between what the system claims to do ("detect conflicts") and what it fully does (detect only exact-time collisions).

**c. Key takeaway**

The biggest lesson was that being the "lead architect" means making the calls the AI can't make for you — like whether `Task` belongs to `Pet` or `Owner` — and then using AI to pressure-test and implement that decision quickly, rather than asking it to make the decision. The UML review step was the clearest example: the AI found real gaps (a missing relationship, a redundant parameter, a data-loss bug), but only because I gave it a specific artifact and a specific question, not an open-ended "build me a scheduler."
