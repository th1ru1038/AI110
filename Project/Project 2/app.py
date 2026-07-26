import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is a pet care planning assistant. Add your pets and their care tasks,
then generate a daily schedule based on priority and available time.
"""
)

# --- Session state: the Owner lives here so it survives Streamlit reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", preferences={"available_minutes": 90})

owner: Owner = st.session_state.owner

st.divider()

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
available_minutes = st.number_input(
    "Available minutes today", min_value=10, max_value=480, value=owner.preferences.get("available_minutes", 90)
)
owner.add_preference("available_minutes", int(available_minutes))

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="")
    age = st.number_input("Age", min_value=0, max_value=40, value=1)
    submitted_pet = st.form_submit_button("Add pet")

if submitted_pet and pet_name:
    owner.add_pet(Pet(name=pet_name, species=species, breed=breed, age=int(age)))
    st.success(f"Added {pet_name} to {owner.name}'s pets.")

if not owner.pets:
    st.info("No pets yet. Add one above.")
else:
    st.divider()
    st.subheader("Add a Task")

    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Pet", pet_names)
    selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)

    with st.form("add_task_form", clear_on_submit=True):
        task_title = st.text_input("Task title", value="Morning walk")
        col1, col2, col3 = st.columns(3)
        with col1:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with col3:
            category = st.selectbox(
                "Category", ["walk", "feeding", "meds", "enrichment", "grooming", "other"]
            )
        col4, col5 = st.columns(2)
        with col4:
            recurrence = st.selectbox("Recurrence", ["daily", "weekly", "one-off"])
        with col5:
            preferred_time = st.text_input("Preferred time (HH:MM, optional)", value="")
        submitted_task = st.form_submit_button("Add task")

    if submitted_task and task_title:
        selected_pet.add_task(
            Task(
                name=task_title,
                duration_minutes=int(duration),
                priority=priority,
                category=category,
                recurrence=recurrence,
                preferred_time=preferred_time or None,
            )
        )
        st.success(f"Added '{task_title}' to {selected_pet.name}.")

    st.markdown(f"### {selected_pet.name}'s tasks")
    status_filter = st.selectbox("Filter by status", ["all", "pending", "completed"])
    visible_tasks = (
        selected_pet.tasks
        if status_filter == "all"
        else [task for task in selected_pet.tasks if task.status == status_filter]
    )

    if not visible_tasks:
        st.info("No tasks match this filter.")
    for task in visible_tasks:
        cols = st.columns([3, 1, 1, 1, 2])
        cols[0].write(task.name)
        cols[1].write(task.priority)
        cols[2].write(f"{task.duration_minutes} min")
        cols[3].write(task.status)
        if task.status == "pending":
            if cols[4].button("Mark complete", key=f"complete-{id(task)}"):
                next_task = selected_pet.complete_task(task)
                if next_task is not None:
                    st.success(f"Completed. Next '{next_task.name}' scheduled for {next_task.due_date}.")
                else:
                    st.success("Completed.")
                st.rerun()

    st.divider()

    st.subheader("Generate Today's Schedule")
    if st.button("Generate schedule"):
        scheduler = Scheduler(available_minutes=int(available_minutes))
        for pet in owner.pets:
            if not pet.tasks:
                continue
            plan = scheduler.generate_plan(pet, available_minutes=int(available_minutes))
            st.markdown(f"**{pet.name}'s schedule**")
            for warning in plan.conflict_warnings:
                st.warning(warning)
            st.code(plan.to_display_string())
            with st.expander("Why this plan?"):
                st.write(plan.explain())
