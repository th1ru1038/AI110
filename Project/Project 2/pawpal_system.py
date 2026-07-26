"""
PawPal+ logic layer.

Backend classes for owners, pets, tasks, and daily-plan scheduling.
No UI code lives here — see app.py for the Streamlit front end.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
RECURRENCE_DELTAS = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: str
    category: str
    recurrence: str
    preferred_time: str | None = None
    due_date: date | None = None
    status: str = "pending"

    def conflicts_with(self, other: "Task") -> bool:
        """Return True if this task and another task share the same preferred time."""
        if self.preferred_time is None or other.preferred_time is None:
            return False
        return self.preferred_time == other.preferred_time

    def to_dict(self) -> dict:
        """Return this task's fields as a plain dict for display or serialization."""
        return {
            "name": self.name,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "category": self.category,
            "recurrence": self.recurrence,
            "preferred_time": self.preferred_time,
            "due_date": self.due_date,
            "status": self.status,
        }

    def mark_complete(self) -> None:
        """Mark this task's status as completed."""
        self.status = "completed"

    def next_occurrence(self) -> "Task | None":
        """Return a fresh pending Task for the next occurrence, or None for one-off tasks."""
        delta = RECURRENCE_DELTAS.get(self.recurrence)
        if delta is None:
            return None
        next_due = (self.due_date or date.today()) + delta
        return Task(
            name=self.name,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            recurrence=self.recurrence,
            preferred_time=self.preferred_time,
            due_date=next_due,
            status="pending",
        )


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def complete_task(self, task: Task) -> "Task | None":
        """Mark a task complete and, if it recurs, add its next occurrence to this pet's tasks."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            self.add_task(next_task)
        return next_task


class Owner:
    def __init__(self, name: str, preferences: dict | None = None):
        """Create an owner with a name and optional scheduling preferences."""
        self.name = name
        self.preferences = preferences or {}
        self.pets: list[Pet] = []

    def add_preference(self, key: str, value) -> None:
        """Set or update a single scheduling preference."""
        self.preferences[key] = value

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Aggregate tasks across every pet this owner has (Owner performs Task)."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def filter_tasks(self, pet_name: str | None = None, status: str | None = None) -> list[Task]:
        """Filter tasks across all pets by pet name and/or completion status."""
        tasks = []
        for pet in self.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            tasks.extend(pet.tasks)
        if status is not None:
            tasks = [task for task in tasks if task.status == status]
        return tasks


class Schedule:
    def __init__(self, pet: Pet):
        """Create an empty schedule for a single pet."""
        self.pet = pet
        self.scheduled_tasks: list[tuple[str, Task]] = []
        self.total_time_used: int = 0
        self.skipped_tasks: list[Task] = []
        self.conflict_warnings: list[str] = []

    def add_task(self, task: Task, time_slot: str) -> None:
        """Add a task to the schedule at the given time slot and track time used."""
        self.scheduled_tasks.append((time_slot, task))
        self.total_time_used += task.duration_minutes

    def to_display_string(self) -> str:
        """Render this schedule as a human-readable, terminal-friendly string."""
        lines = [f"Today's Schedule for {self.pet.name} ({self.pet.breed}):"]
        for time_slot, task in self.scheduled_tasks:
            lines.append(
                f"  {time_slot} — {task.name} ({task.duration_minutes} min) [priority: {task.priority}]"
            )
        if self.skipped_tasks:
            lines.append("  Not scheduled (time ran out or a conflict was detected):")
            for task in self.skipped_tasks:
                lines.append(f"    - {task.name} ({task.duration_minutes} min)")
        for warning in self.conflict_warnings:
            lines.append(f"  ⚠ {warning}")
        return "\n".join(lines)

    def explain(self) -> str:
        """Render a plain-language explanation of why each task was scheduled or skipped."""
        lines = [f"{self.total_time_used} minutes scheduled for {self.pet.name}."]
        for time_slot, task in self.scheduled_tasks:
            lines.append(
                f"- {task.name} was scheduled at {time_slot} because it has "
                f"{task.priority} priority."
            )
        for task in self.skipped_tasks:
            lines.append(f"- {task.name} was not scheduled: no time left, or its preferred time conflicted with a higher-priority task.")
        return "\n".join(lines)


class Scheduler:
    def __init__(self, available_minutes: int, constraints: dict | None = None):
        """Create a scheduler with a default time budget and optional constraints."""
        self.available_minutes = available_minutes
        self.constraints = constraints or {}

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority (high first), then by shorter duration."""
        return sorted(
            tasks,
            key=lambda task: (PRIORITY_ORDER.get(task.priority, 99), task.duration_minutes),
        )

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks chronologically by preferred_time ('HH:MM'); tasks with no time sort last."""
        return sorted(
            tasks,
            key=lambda task: (task.preferred_time is None, task.preferred_time or ""),
        )

    def filter_tasks(self, tasks: list[Task], time_budget: int) -> list[Task]:
        """Keep tasks in order until the time budget would be exceeded."""
        kept = []
        remaining = time_budget
        for task in tasks:
            if task.duration_minutes <= remaining:
                kept.append(task)
                remaining -= task.duration_minutes
        return kept

    def filter_by_status(self, tasks: list[Task], status: str) -> list[Task]:
        """Return only the tasks matching the given status (e.g. 'pending', 'completed')."""
        return [task for task in tasks if task.status == status]

    def resolve_conflicts(self, tasks: list[Task]) -> list[Task]:
        """Drop later tasks that share a preferred time already claimed by an earlier task."""
        resolved: list[Task] = []
        seen_times: set[str] = set()
        for task in tasks:
            if task.preferred_time and task.preferred_time in seen_times:
                continue
            if task.preferred_time:
                seen_times.add(task.preferred_time)
            resolved.append(task)
        return resolved

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return human-readable warnings for tasks that share the same preferred time.

        Lightweight by design: only exact HH:MM matches are flagged, not overlapping
        durations. This never raises — it just returns warning strings for the caller
        (CLI or UI) to display.
        """
        warnings: list[str] = []
        seen: dict[str, Task] = {}
        for task in tasks:
            if not task.preferred_time:
                continue
            existing = seen.get(task.preferred_time)
            if existing is not None:
                warnings.append(
                    f"'{task.name}' and '{existing.name}' are both scheduled at "
                    f"{task.preferred_time}."
                )
            else:
                seen[task.preferred_time] = task
        return warnings

    def generate_plan(self, pet: Pet, available_minutes: int) -> Schedule:
        """Build a full daily Schedule for a pet by sorting, deconflicting, and filtering its tasks."""
        sorted_tasks = self.sort_tasks(pet.tasks)
        warnings = self.detect_conflicts(sorted_tasks)
        conflict_free = self.resolve_conflicts(sorted_tasks)
        fitted = self.filter_tasks(conflict_free, available_minutes)

        schedule = Schedule(pet)
        for task in fitted:
            time_slot = task.preferred_time or "unscheduled"
            schedule.add_task(task, time_slot)
        schedule.skipped_tasks = [
            task for task in pet.tasks if task not in fitted and task.status != "completed"
        ]
        schedule.conflict_warnings = warnings
        return schedule
