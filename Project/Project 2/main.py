"""
Temporary terminal testing ground for PawPal+ logic.
Not part of the final app — used to sanity-check pawpal_system.py before wiring up app.py.
"""

from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Jordan", preferences={"available_minutes": 90})

biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
mochi = Pet(name="Mochi", species="cat", breed="Tabby", age=2)

owner.add_pet(biscuit)
owner.add_pet(mochi)

# Tasks added out of time order on purpose, to exercise sort_by_time().
biscuit.add_task(
    Task(
        name="Feeding",
        duration_minutes=10,
        priority="high",
        category="feeding",
        recurrence="daily",
        preferred_time="09:00",
    )
)
biscuit.add_task(
    Task(
        name="Morning walk",
        duration_minutes=30,
        priority="high",
        category="walk",
        recurrence="daily",
        preferred_time="08:00",
    )
)
# Deliberate conflict: same preferred_time as "Morning walk", to exercise detect_conflicts().
biscuit.add_task(
    Task(
        name="Meds",
        duration_minutes=5,
        priority="high",
        category="meds",
        recurrence="daily",
        preferred_time="08:00",
    )
)
mochi.add_task(
    Task(
        name="Grooming",
        duration_minutes=20,
        priority="medium",
        category="grooming",
        recurrence="weekly",
        preferred_time="10:00",
    )
)

scheduler = Scheduler(available_minutes=90)

print("=== Tasks sorted by time (Biscuit) ===")
for task in scheduler.sort_by_time(biscuit.tasks):
    print(f"  {task.preferred_time} — {task.name}")
print()

print("=== Today's schedules ===")
for pet in owner.pets:
    plan = scheduler.generate_plan(pet, available_minutes=owner.preferences["available_minutes"])
    print(plan.to_display_string())
    print()

print("=== Recurring task demo ===")
walk = biscuit.tasks[0] if biscuit.tasks[0].name == "Morning walk" else biscuit.tasks[1]
next_walk = biscuit.complete_task(walk)
print(f"Completed '{walk.name}' (status={walk.status})")
if next_walk:
    print(f"Next occurrence auto-created: '{next_walk.name}' due {next_walk.due_date}")

print()
print("=== Filtering demo (pending tasks for Biscuit) ===")
pending = owner.filter_tasks(pet_name="Biscuit", status="pending")
for task in pending:
    print(f"  {task.name} ({task.status})")
