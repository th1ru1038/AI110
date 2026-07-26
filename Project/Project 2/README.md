# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

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
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
collected 2 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 50%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [100%]

============================== 2 passed in 0.02s ===============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting (priority) | `Scheduler.sort_tasks()` | Sorts by priority (high → low), then by shorter duration as a tiebreaker |
| Task sorting (time) | `Scheduler.sort_by_time()` | Sorts chronologically by `preferred_time` ("HH:MM"); tasks with no time sort last |
| Filtering | `Scheduler.filter_tasks()`, `Scheduler.filter_by_status()`, `Owner.filter_tasks()` | Drops tasks once the time budget runs out; filters by completion status and/or pet name |
| Conflict handling | `Scheduler.detect_conflicts()`, `Scheduler.resolve_conflicts()` | Flags tasks sharing an exact `preferred_time` as a warning, and drops the lower-priority one from the generated schedule (does not check overlapping durations — see reflection 2b) |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Completing a `daily`/`weekly` task auto-creates its next occurrence using `datetime.timedelta` |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
