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

1. **Added `Owner.all_tasks()`.** The UML said `Owner performs Task`, but the code  no way to actually reach an owner's tasks — you'd have had to mhadanually loop through `owner.pets[i].tasks` yourself. Added a method that aggregates tasks across all of an owner's pets so that relationship is real in code, not just implied on the diagram.
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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
