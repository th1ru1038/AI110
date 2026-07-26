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

for pet in owner.pets:
    plan = scheduler.generate_plan(pet, available_minutes=owner.preferences["available_minutes"])
    print(plan.to_display_string())
    print()
