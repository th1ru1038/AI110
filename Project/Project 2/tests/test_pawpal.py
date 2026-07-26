from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_task(name, duration=10, priority="medium", preferred_time=None, recurrence="one-off", due_date=None):
    return Task(
        name=name,
        duration_minutes=duration,
        priority=priority,
        category="walk",
        recurrence=recurrence,
        preferred_time=preferred_time,
        due_date=due_date,
    )


# --- Happy path: basic object behavior ---


def test_mark_complete_changes_status():
    task = make_task("Morning walk")
    assert task.status == "pending"

    task.mark_complete()

    assert task.status == "completed"


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
    assert len(pet.tasks) == 0

    pet.add_task(make_task("Feeding"))

    assert len(pet.tasks) == 1


# --- Sorting correctness ---


def test_sort_tasks_orders_by_priority_then_duration():
    scheduler = Scheduler(available_minutes=60)
    low = make_task("Enrichment", duration=15, priority="low")
    high_long = make_task("Walk", duration=30, priority="high")
    high_short = make_task("Meds", duration=5, priority="high")

    sorted_tasks = scheduler.sort_tasks([low, high_long, high_short])

    assert [task.name for task in sorted_tasks] == ["Meds", "Walk", "Enrichment"]


def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler(available_minutes=60)
    late = make_task("Grooming", preferred_time="15:00")
    early = make_task("Walk", preferred_time="08:00")
    no_time = make_task("Enrichment", preferred_time=None)

    sorted_tasks = scheduler.sort_by_time([late, early, no_time])

    assert [task.name for task in sorted_tasks] == ["Walk", "Grooming", "Enrichment"]


# --- Filtering ---


def test_filter_tasks_drops_tasks_once_budget_exceeded():
    scheduler = Scheduler(available_minutes=15)
    tasks = [make_task("A", duration=10), make_task("B", duration=10)]

    kept = scheduler.filter_tasks(tasks, time_budget=15)

    assert [task.name for task in kept] == ["A"]


def test_owner_filter_tasks_by_pet_and_status():
    owner = Owner(name="Jordan")
    biscuit = Pet(name="Biscuit", species="dog", breed="Lab", age=2)
    mochi = Pet(name="Mochi", species="cat", breed="Tabby", age=1)
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    biscuit_task = make_task("Walk")
    biscuit_task.mark_complete()
    biscuit.add_task(biscuit_task)
    biscuit.add_task(make_task("Feeding"))
    mochi.add_task(make_task("Grooming"))

    pending_for_biscuit = owner.filter_tasks(pet_name="Biscuit", status="pending")

    assert [task.name for task in pending_for_biscuit] == ["Feeding"]


# --- Conflict detection ---


def test_detect_conflicts_flags_duplicate_preferred_times():
    scheduler = Scheduler(available_minutes=60)
    walk = make_task("Walk", preferred_time="08:00")
    meds = make_task("Meds", preferred_time="08:00")

    warnings = scheduler.detect_conflicts([walk, meds])

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_detect_conflicts_returns_empty_list_when_no_conflicts():
    scheduler = Scheduler(available_minutes=60)
    walk = make_task("Walk", preferred_time="08:00")
    meds = make_task("Meds", preferred_time="09:00")

    warnings = scheduler.detect_conflicts([walk, meds])

    assert warnings == []


# --- Recurrence logic ---


def test_complete_daily_task_creates_next_occurrence_one_day_later():
    pet = Pet(name="Biscuit", species="dog", breed="Lab", age=2)
    today = date(2026, 7, 25)
    task = make_task("Walk", recurrence="daily", due_date=today)
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.status == "completed"
    assert next_task is not None
    assert next_task.status == "pending"
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task in pet.tasks


def test_complete_one_off_task_does_not_create_next_occurrence():
    pet = Pet(name="Biscuit", species="dog", breed="Lab", age=2)
    task = make_task("Vet visit", recurrence="one-off")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is None
    assert len(pet.tasks) == 1


# --- Edge cases ---


def test_generate_plan_for_pet_with_no_tasks_returns_empty_schedule():
    pet = Pet(name="Biscuit", species="dog", breed="Lab", age=2)
    scheduler = Scheduler(available_minutes=60)

    schedule = scheduler.generate_plan(pet, available_minutes=60)

    assert schedule.scheduled_tasks == []
    assert schedule.skipped_tasks == []
    assert schedule.total_time_used == 0


def test_generate_plan_warns_and_drops_lower_priority_conflicting_task():
    pet = Pet(name="Biscuit", species="dog", breed="Lab", age=2)
    pet.add_task(make_task("Meds", duration=5, priority="high", preferred_time="08:00"))
    pet.add_task(make_task("Walk", duration=30, priority="low", preferred_time="08:00"))
    scheduler = Scheduler(available_minutes=60)

    schedule = scheduler.generate_plan(pet, available_minutes=60)

    scheduled_names = [task.name for _, task in schedule.scheduled_tasks]
    assert scheduled_names == ["Meds"]
    assert any(task.name == "Walk" for task in schedule.skipped_tasks)
    assert len(schedule.conflict_warnings) == 1
