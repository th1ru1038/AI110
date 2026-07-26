# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## ✨ Features

- **Owner + multi-pet tracking** — one owner can manage multiple pets, each with its own task list
- **Task management** — add tasks with duration, priority, category, recurrence, and an optional preferred time
- **Smart scheduling** — sorts tasks by priority (and, separately, by time), fits as many as possible into an available-minutes budget, and explains why each task was scheduled or skipped
- **Conflict warnings** — flags tasks that share the same preferred time instead of silently overwriting one, so the owner can resolve the overlap themselves
- **Recurring tasks** — marking a daily/weekly task complete automatically creates its next occurrence
- **Filtering** — view tasks by pet and/or completion status
- **Persistent session** — the Streamlit UI keeps all owner/pet/task data in `st.session_state` so it survives interaction reruns

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`, which builds an Owner with two Pets and generates a daily schedule for each:

```
=== Tasks sorted by time (Biscuit) ===
  08:00 — Morning walk
  08:00 — Meds
  09:00 — Feeding

=== Today's schedules ===
Today's Schedule for Biscuit (Golden Retriever):
  08:00 — Meds (5 min) [priority: high]
  09:00 — Feeding (10 min) [priority: high]
  Not scheduled (time ran out or a conflict was detected):
    - Morning walk (30 min)
  ⚠ 'Morning walk' and 'Meds' are both scheduled at 08:00.

Today's Schedule for Mochi (Tabby):
  10:00 — Grooming (20 min) [priority: medium]

=== Recurring task demo ===
Completed 'Morning walk' (status=completed)
Next occurrence auto-created: 'Morning walk' due 2026-07-26

=== Filtering demo (pending tasks for Biscuit) ===
  Feeding (pending)
  Meds (pending)
  Morning walk (pending)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

`tests/test_pawpal.py` covers:
- **Object basics**: `mark_complete()` changes status, `Pet.add_task()` increases task count
- **Sorting**: `sort_tasks()` orders by priority then duration; `sort_by_time()` orders chronologically
- **Filtering**: `filter_tasks()` respects the time budget; `Owner.filter_tasks()` filters by pet + status
- **Conflict detection**: `detect_conflicts()` flags duplicate preferred times and returns no warnings when there's no overlap
- **Recurring tasks**: completing a `daily` task creates a next occurrence one day later (via `timedelta`); completing a `one-off` task does not
- **Edge cases**: a pet with no tasks produces an empty schedule; a low-priority task that conflicts with a higher-priority one at the same time gets dropped and generates exactly one warning

Sample test output:

```
============================= test session starts ==============================
collected 12 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  8%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 16%]
tests/test_pawpal.py::test_sort_tasks_orders_by_priority_then_duration PASSED [ 25%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 33%]
tests/test_pawpal.py::test_filter_tasks_drops_tasks_once_budget_exceeded PASSED [ 41%]
tests/test_pawpal.py::test_owner_filter_tasks_by_pet_and_status PASSED   [ 50%]
tests/test_pawpal.py::test_detect_conflicts_flags_duplicate_preferred_times PASSED [ 58%]
tests/test_pawpal.py::test_detect_conflicts_returns_empty_list_when_no_conflicts PASSED [ 66%]
tests/test_pawpal.py::test_complete_daily_task_creates_next_occurrence_one_day_later PASSED [ 75%]
tests/test_pawpal.py::test_complete_one_off_task_does_not_create_next_occurrence PASSED [ 83%]
tests/test_pawpal.py::test_generate_plan_for_pet_with_no_tasks_returns_empty_schedule PASSED [ 91%]
tests/test_pawpal.py::test_generate_plan_warns_and_drops_lower_priority_conflicting_task PASSED [100%]

============================== 12 passed in 0.02s ===============================
```

**Confidence level:** ⭐⭐⭐⭐☆ (4/5) — core sorting, filtering, conflict-flagging, and recurrence behaviors are covered and passing. Not yet tested: overlapping-duration conflicts (see `reflection.md` 2b), multi-pet schedule generation together in one run, and Streamlit UI interactions (session-state persistence across reruns is exercised manually, not by automated tests).

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting (priority) | `Scheduler.sort_tasks()` | Sorts by priority (high → low), then by shorter duration as a tiebreaker |
| Task sorting (time) | `Scheduler.sort_by_time()` | Sorts chronologically by `preferred_time` ("HH:MM"); tasks with no time sort last |
| Filtering | `Scheduler.filter_tasks()`, `Scheduler.filter_by_status()`, `Owner.filter_tasks()` | Drops tasks once the time budget runs out; filters by completion status and/or pet name |
| Conflict handling | `Scheduler.detect_conflicts()`, `Scheduler.resolve_conflicts()` | Flags tasks sharing an exact `preferred_time` as a warning, and drops the lower-priority one from the generated schedule (does not check overlapping durations — see reflection 2b) |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Completing a `daily`/`weekly` task auto-creates its next occurrence using `datetime.timedelta` |

## 📸 Demo Walkthrough

1. **Set owner info.** Enter the owner's name and how many minutes are available today. This value drives the scheduler's time budget.
2. **Add a pet.** Fill in the "Add a Pet" form (name, species, breed, age) and submit — the pet appears immediately and becomes selectable.
3. **Add tasks to a pet.** Select a pet from the dropdown, then use "Add a Task" to add care tasks with a duration, priority, category, recurrence (daily/weekly/one-off), and an optional preferred time (e.g. `08:00`).
4. **View and filter tasks.** The task list below the form can be filtered by status (all/pending/completed). Each pending task has a "Mark complete" button.
5. **Mark a recurring task complete.** Clicking "Mark complete" on a `daily`/`weekly` task automatically creates its next occurrence — you'll see a confirmation naming the new due date, and the new task appears back in the pending list.
6. **Generate today's schedule.** Click "Generate schedule" to run the `Scheduler` for every pet. Each pet gets its own schedule block: any detected time conflicts show as a warning banner, followed by the ordered plan, followed by an expandable "Why this plan?" explanation.

**Key Scheduler behaviors shown:** priority-based sorting (`sort_tasks`), the time budget cutting off lower-priority tasks once minutes run out (`filter_tasks`), and same-time conflicts being flagged rather than silently dropped (`detect_conflicts`).

Sample CLI output from `python main.py` (same underlying logic as the UI, run outside Streamlit):

```
=== Tasks sorted by time (Biscuit) ===
  08:00 — Morning walk
  08:00 — Meds
  09:00 — Feeding

=== Today's schedules ===
Today's Schedule for Biscuit (Golden Retriever):
  08:00 — Meds (5 min) [priority: high]
  09:00 — Feeding (10 min) [priority: high]
  Not scheduled (time ran out or a conflict was detected):
    - Morning walk (30 min)
  ⚠ 'Morning walk' and 'Meds' are both scheduled at 08:00.

Today's Schedule for Mochi (Tabby):
  10:00 — Grooming (20 min) [priority: medium]

=== Recurring task demo ===
Completed 'Morning walk' (status=completed)
Next occurrence auto-created: 'Morning walk' due 2026-07-26

=== Filtering demo (pending tasks for Biscuit) ===
  Feeding (pending)
  Meds (pending)
  Morning walk (pending)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
