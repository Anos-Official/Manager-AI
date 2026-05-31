import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import threading
import customtkinter as ctk
from Backend.Ai.ai import ask_ai

TASK_SYSTEM_PROMPT = """You are a productivity coach for Manager AI.
You help users stay focused and productive by recommending specific daily tasks.
Be concise, practical, and motivating. Always recommend 5-7 specific actionable tasks for today."""

preset_goals = [
    {
        "title": "Learn Python",
        "tasks": [
            {"title": "Complete beginner tutorials", "items": ["Watch Python basics on YouTube", "Complete freeCodeCamp Python course"]},
            {"title": "Build a small project", "items": ["Plan the project idea", "Write the first 50 lines of code"]},
        ]
    },
    {
        "title": "Persuade Mr. Scott to Get More RAM",
        "tasks": [
            {"title": "Build the case", "items": ["Research RAM prices in Canada", "Calculate performance improvement", "Prepare a PowerPoint presentation"]},
            {"title": "Execute the plan", "items": ["Schedule a meeting with Mr. Scott", "Present the evidence", "Send a follow-up email with Amazon links"]},
        ]
    },
    {
        "title": "Career Development",
        "tasks": [
            {"title": "Update resume", "items": ["Add recent projects", "Fix formatting"]},
            {"title": "Research job postings", "items": ["Check LinkedIn", "Check Indeed.ca"]},
        ]
    }
]

def create(parent):
    frame = ctk.CTkFrame(parent, fg_color="#323339", corner_radius=0)
    font = lambda size, bold=False: ctk.CTkFont(family="Nunito", size=size, weight="bold" if bold else "normal")

    # header
    header = ctk.CTkFrame(frame, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(20,5))

    ctk.CTkLabel(header, text="Tasks & Goals", font=font(26, bold=True)).pack(side="left")

    add_goal_btn = ctk.CTkButton(header, text="+ Add Goal", width=120, font=font(13, bold=True))
    add_goal_btn.pack(side="right")

    # main scroll
    scroll = ctk.CTkScrollableFrame(frame, fg_color="#323339")
    scroll.pack(fill="both", expand=True, padx=20, pady=5)

    goals_data = [dict(g) for g in preset_goals]

    def render_goals():
        for w in scroll.winfo_children():
            if hasattr(w, '_is_goal'):
                w.destroy()

        for g_index, goal in enumerate(goals_data):
            goal_container = ctk.CTkFrame(scroll, fg_color="#2C2D32", corner_radius=8)
            goal_container._is_goal = True
            goal_container.pack(fill="x", pady=5)

            # goal header row
            goal_header = ctk.CTkFrame(goal_container, fg_color="transparent")
            goal_header.pack(fill="x", padx=10, pady=5)

            expanded = [True]

            tasks_container = ctk.CTkFrame(goal_container, fg_color="transparent")
            tasks_container.pack(fill="x", padx=10, pady=5)

            def toggle(tc=tasks_container, e=expanded):
                if e[0]:
                    tc.pack_forget()
                    e[0] = False
                else:
                    tc.pack(fill="x", padx=10, pady=5)
                    e[0] = True

            ctk.CTkButton(goal_header, text="▼", width=30, fg_color="transparent",
                          hover_color="#121212", font=font(13), command=toggle).pack(side="left")

            ctk.CTkLabel(goal_header, text=goal["title"],
                         font=font(16, bold=True)).pack(side="left", padx=5)

            def remove_goal(i=g_index):
                goals_data.pop(i)
                render_goals()

            ctk.CTkButton(goal_header, text="✕", width=30, fg_color="transparent",
                          hover_color="#ff4444", font=font(13),
                          command=remove_goal).pack(side="right")

            ctk.CTkButton(goal_header, text="+ Task", width=70, fg_color="transparent",
                          hover_color="#121212", font=font(12),
                          command=lambda i=g_index: add_task_popup(i)).pack(side="right", padx=5)

            # tasks
            for t_index, task in enumerate(goal.get("tasks", [])):
                task_frame = ctk.CTkFrame(tasks_container, fg_color="#323339", corner_radius=6)
                task_frame.pack(fill="x", pady=3)

                task_header = ctk.CTkFrame(task_frame, fg_color="transparent")
                task_header.pack(fill="x", padx=8, pady=3)

                ctk.CTkLabel(task_header, text=task["title"],
                             font=font(14, bold=True)).pack(side="left")

                def remove_task(gi=g_index, ti=t_index):
                    goals_data[gi]["tasks"].pop(ti)
                    render_goals()

                ctk.CTkButton(task_header, text="✕", width=25, fg_color="transparent",
                              hover_color="#ff4444", font=font(12),
                              command=remove_task).pack(side="right")

                # checklist items
                for item in task.get("items", []):
                    item_row = ctk.CTkFrame(task_frame, fg_color="transparent")
                    item_row.pack(fill="x", padx=15, pady=1)
                    var = ctk.BooleanVar()
                    ctk.CTkCheckBox(item_row, text=item, variable=var,
                                    font=font(12)).pack(side="left")

    def add_task_popup(goal_index):
        popup = ctk.CTkToplevel()
        popup.title("Add Task")
        popup.geometry("400x300")
        popup.configure(fg_color="#323339")

        ctk.CTkLabel(popup, text="Task Title", font=font(13)).pack(pady=(20,5))
        task_entry = ctk.CTkEntry(popup, width=300, font=font(13))
        task_entry.pack()

        ctk.CTkLabel(popup, text="Checklist Items (one per line)", font=font(13)).pack(pady=(15,5))
        items_box = ctk.CTkTextbox(popup, width=300, height=100, font=font(13))
        items_box.pack()

        def confirm():
            title = task_entry.get().strip()
            items = [l.strip() for l in items_box.get("1.0", "end").split("\n") if l.strip()]
            if title:
                goals_data[goal_index]["tasks"].append({"title": title, "items": items})
                render_goals()
                popup.destroy()

        ctk.CTkButton(popup, text="Add Task", command=confirm, font=font(13, bold=True)).pack(pady=15)

    def add_goal_action():
        popup = ctk.CTkToplevel()
        popup.title("Add Goal")
        popup.geometry("400x200")
        popup.configure(fg_color="#323339")

        ctk.CTkLabel(popup, text="Goal Title", font=font(13)).pack(pady=(20,5))
        goal_entry = ctk.CTkEntry(popup, width=300, font=font(13))
        goal_entry.pack()

        def confirm():
            title = goal_entry.get().strip()
            if title:
                goals_data.append({"title": title, "tasks": []})
                render_goals()
                popup.destroy()

        ctk.CTkButton(popup, text="Add Goal", command=confirm, font=font(13, bold=True)).pack(pady=15)

    add_goal_btn.configure(command=add_goal_action)

    # AI daily tasks section
    ctk.CTkLabel(frame, text="AI Daily Tasks", font=font(18, bold=True)).pack(anchor="w", padx=20, pady=(10,5))

    ai_frame = ctk.CTkFrame(frame, fg_color="#2C2D32", corner_radius=8)
    ai_frame.pack(fill="x", padx=20, pady=5)

    ai_box = ctk.CTkTextbox(ai_frame, height=150, state="disabled", font=font(13))
    ai_box.pack(fill="x", padx=10, pady=10)

    ai_btn = ctk.CTkButton(frame, text="Get AI Daily Tasks", font=font(14, bold=True))
    ai_btn.pack(pady=10)

    def get_ai_tasks():
        ai_btn.configure(state="disabled", text="Loading...")
        def run():
            goals_summary = ""
            for goal in goals_data:
                goals_summary += f"\nGoal: {goal['title']}\n"
                for task in goal.get("tasks", []):
                    goals_summary += f"  - {task['title']}\n"

            prompt = f"""Based on these goals and tasks, recommend 5-7 specific things this person should focus on today:
{goals_summary}
Be specific, actionable, and prioritized."""
            result = ask_ai(prompt, system_prompt=TASK_SYSTEM_PROMPT)
            ai_box.configure(state="normal")
            ai_box.delete("1.0", "end")
            ai_box.insert("end", result)
            ai_box.configure(state="disabled")
            ai_btn.configure(state="normal", text="Get AI Daily Tasks")
        threading.Thread(target=run).start()

    ai_btn.configure(command=get_ai_tasks)

    render_goals()
    return frame