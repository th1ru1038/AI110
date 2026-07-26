from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    task = Task(
        name="Morning walk",
        duration_minutes=30,
        priority="high",
        category="walk",
        recurrence="daily",
    )
    assert task.status == "pending"

    task.mark_complete()

    assert task.status == "completed"


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
    assert len(pet.tasks) == 0

    pet.add_task(
        Task(
            name="Feeding",
            duration_minutes=10,
            priority="high",
            category="feeding",
            recurrence="daily",
        )
    )

    assert len(pet.tasks) == 1
