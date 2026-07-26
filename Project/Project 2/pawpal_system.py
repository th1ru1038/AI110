"""
PawPal+ logic layer.

Backend classes for owners, pets, tasks, and daily-plan scheduling.
No UI code lives here — see app.py for the Streamlit front end.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: str
    category: str
    recurrence: str
    preferred_time: str | None = None

    def conflicts_with(self, other: "Task") -> bool:
        pass

    def to_dict(self) -> dict:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


class Owner:
    def __init__(self, name: str, preferences: dict | None = None):
        self.name = name
        self.preferences = preferences or {}
        self.pets: list[Pet] = []

    def add_preference(self, key: str, value) -> None:
        pass

    def add_pet(self, pet: Pet) -> None:
        pass

    def all_tasks(self) -> list[Task]:
        """Aggregate tasks across every pet this owner has (Owner performs Task)."""
        pass


class Schedule:
    def __init__(self, pet: Pet):
        self.pet = pet
        self.scheduled_tasks: list[tuple[str, Task]] = []
        self.total_time_used: int = 0
        self.skipped_tasks: list[Task] = []

    def add_task(self, task: Task, time_slot: str) -> None:
        pass

    def to_display_string(self) -> str:
        pass

    def explain(self) -> str:
        pass


class Scheduler:
    def __init__(self, available_minutes: int, constraints: dict | None = None):
        self.available_minutes = available_minutes
        self.constraints = constraints or {}

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        pass

    def filter_tasks(self, tasks: list[Task], time_budget: int) -> list[Task]:
        pass

    def resolve_conflicts(self, tasks: list[Task]) -> list[Task]:
        pass

    def generate_plan(self, pet: Pet, available_minutes: int) -> Schedule:
        pass
