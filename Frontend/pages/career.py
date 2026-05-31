import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import threading
import customtkinter as ctk
from tkinter import filedialog
from Backend.Career.career_ai import get_career_suggestions, get_roadmap, get_skills_gap, extract_profile_from_resume
from Frontend.utils import render_markdown

# state
profile = {
    "resume_path": None,
    "name": "",
    "education": "",
    "skills": "",
    "career_goal": "",
    "checklist": []
}

def create(parent):
    frame = ctk.CTkFrame(parent, fg_color="#323339", corner_radius=0)

    # ── Progress bar ──────────────────────────────────────────────────────────
    progress_frame = ctk.CTkFrame(frame, fg_color="#2B2C31", height=50, corner_radius=0)
    progress_frame.pack(fill="x")
    progress_frame.pack_propagate(False)

    step1_lbl = ctk.CTkLabel(progress_frame, text="1. Profile",
                              font=ctk.CTkFont(family="Nunito", size=14, weight="bold"))
    step1_lbl.pack(side="left", padx=30, pady=10)

    ctk.CTkLabel(progress_frame, text="→", font=ctk.CTkFont(size=14)).pack(side="left")

    step2_lbl = ctk.CTkLabel(progress_frame, text="2. Career Goal",
                              font=ctk.CTkFont(family="Nunito", size=14))
    step2_lbl.pack(side="left", padx=30, pady=10)

    ctk.CTkLabel(progress_frame, text="→", font=ctk.CTkFont(size=14)).pack(side="left")

    step3_lbl = ctk.CTkLabel(progress_frame, text="3. Roadmap",
                              font=ctk.CTkFont(family="Nunito", size=14))
    step3_lbl.pack(side="left", padx=30, pady=10)

    # ── Content area ──────────────────────────────────────────────────────────
    content = ctk.CTkFrame(frame, fg_color="#323339")
    content.pack(fill="both", expand=True)

    # ── STEP 1: Profile ───────────────────────────────────────────────────────
    step1_frame = ctk.CTkFrame(content, fg_color="#323339")

    ctk.CTkLabel(step1_frame, text="Set Up Your Profile",
                 font=ctk.CTkFont(family="Nunito", size=24, weight="bold")).pack(pady=20)

    resume_lbl = ctk.CTkLabel(step1_frame, text="No resume uploaded",
                               font=ctk.CTkFont(family="Nunito", size=13))
    resume_lbl.pack(pady=5)

    def upload_resume():
        path = filedialog.askopenfilename(filetypes=[("Resume files", "*.pdf *.docx")])
        if path:
            profile["resume_path"] = path
            resume_lbl.configure(text=f"✓ {os.path.basename(path)}")

    ctk.CTkButton(step1_frame, text="Upload Resume (PDF or Word)", command=upload_resume,
                  font=ctk.CTkFont(family="Nunito", size=13)).pack(pady=5)

    ctk.CTkLabel(step1_frame, text="Full Name",
                 font=ctk.CTkFont(family="Nunito", size=13)).pack(pady=(15, 2))
    name_entry = ctk.CTkEntry(step1_frame, width=400, placeholder_text="e.g. Jordan Scott")
    name_entry.pack()

    ctk.CTkLabel(step1_frame, text="Education Level",
                 font=ctk.CTkFont(family="Nunito", size=13)).pack(pady=(10, 2))
    education_entry = ctk.CTkEntry(step1_frame, width=400,
                                    placeholder_text="e.g. High School, College, University")
    education_entry.pack()

    ctk.CTkLabel(step1_frame, text="Current Skills",
                 font=ctk.CTkFont(family="Nunito", size=13)).pack(pady=(10, 2))
    skills_entry = ctk.CTkEntry(step1_frame, width=400,
                                 placeholder_text="e.g. Python, Excel, Communication")
    skills_entry.pack()

    def go_to_step2():
        profile["name"] = name_entry.get()
        profile["education"] = education_entry.get()
        profile["skills"] = skills_entry.get()
        step1_frame.pack_forget()
        step2_lbl.configure(font=ctk.CTkFont(family="Nunito", size=14, weight="bold"))
        step2_frame.pack(fill="both", expand=True)

    ctk.CTkButton(step1_frame, text="Next →", command=go_to_step2,
                  font=ctk.CTkFont(family="Nunito", size=14, weight="bold")).pack(pady=30)

    # ── STEP 2: Career Goal ───────────────────────────────────────────────────
    step2_frame = ctk.CTkFrame(content, fg_color="#323339")

    ctk.CTkLabel(step2_frame, text="Choose Your Career Goal",
                 font=ctk.CTkFont(family="Nunito", size=24, weight="bold")).pack(pady=20)

    ctk.CTkLabel(step2_frame,
                 text="Type your career goal, or let AI suggest one based on your profile.",
                 font=ctk.CTkFont(family="Nunito", size=13)).pack(pady=5)

    goal_entry = ctk.CTkEntry(step2_frame, width=400,
                               placeholder_text="e.g. Software Developer, Nurse, Electrician")
    goal_entry.pack(pady=10)

    ai_suggestions_box = ctk.CTkTextbox(step2_frame, width=600, height=200, state="disabled",
                                         font=ctk.CTkFont(family="Nunito", size=13))
    ai_suggestions_box.pack(pady=10)

    suggest_btn = ctk.CTkButton(step2_frame, text="Get AI Career Suggestions",
                                 font=ctk.CTkFont(family="Nunito", size=13))
    suggest_btn.pack(pady=5)

    def get_suggestions():
        suggest_btn.configure(state="disabled", text="Loading...")

        def run():
            result = get_career_suggestions(
                interests=profile["skills"],
                skills=profile["skills"],
                education=profile["education"]
            )
            # ✅ Push UI update back to main thread
            def update():
                ai_suggestions_box.configure(state="normal")
                ai_suggestions_box.delete("1.0", "end")
                ai_suggestions_box.insert("end", result)
                ai_suggestions_box.configure(state="disabled")
                suggest_btn.configure(state="normal", text="Get AI Career Suggestions")
            frame.after(0, update)

        threading.Thread(target=run, daemon=True).start()

    suggest_btn.configure(command=get_suggestions)

    def go_to_step3():
        profile["career_goal"] = goal_entry.get()
        if not profile["career_goal"]:
            return
        step2_frame.pack_forget()
        step3_lbl.configure(font=ctk.CTkFont(family="Nunito", size=14, weight="bold"))
        step3_frame.pack(fill="both", expand=True)
        load_roadmap()

    def go_back_to_step1():
        step2_frame.pack_forget()
        step1_frame.pack(fill="both", expand=True)

    btn_row = ctk.CTkFrame(step2_frame, fg_color="transparent")
    btn_row.pack(pady=20)
    ctk.CTkButton(btn_row, text="← Back", command=go_back_to_step1,
                  font=ctk.CTkFont(family="Nunito", size=14)).pack(side="left", padx=10)
    ctk.CTkButton(btn_row, text="Next →", command=go_to_step3,
                  font=ctk.CTkFont(family="Nunito", size=14, weight="bold")).pack(side="left", padx=10)

    # ── STEP 3: Roadmap & Checklist ───────────────────────────────────────────
    step3_frame = ctk.CTkFrame(content, fg_color="#323339")

    ctk.CTkLabel(step3_frame, text="Your Roadmap",
                 font=ctk.CTkFont(family="Nunito", size=24, weight="bold")).pack(pady=20)

    roadmap_box = ctk.CTkTextbox(step3_frame, width=600, height=150, state="disabled",
                                  font=ctk.CTkFont(family="Nunito", size=13))
    roadmap_box.pack(pady=10)

    ctk.CTkLabel(step3_frame, text="Skills Gap Checklist",
                 font=ctk.CTkFont(family="Nunito", size=16, weight="bold")).pack(pady=(10, 5))

    checklist_frame = ctk.CTkScrollableFrame(step3_frame, width=600, height=200, fg_color="#2C2D32")
    checklist_frame.pack(pady=5)

    def load_roadmap():
        # ✅ Show loading state on main thread immediately
        roadmap_box.configure(state="normal")
        roadmap_box.delete("1.0", "end")
        roadmap_box.insert("end", "⏳ Loading your roadmap...")
        roadmap_box.configure(state="disabled")

        for widget in checklist_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(checklist_frame, text="⏳ Loading skills gap...",
                     font=ctk.CTkFont(family="Nunito", size=12)).pack(pady=10)

        def run():
            # Run AI calls in background thread
            roadmap = get_roadmap(profile["career_goal"], profile["skills"])
            gaps = get_skills_gap(
                profile["career_goal"],
                profile["skills"],
                profile.get("resume_path")
            )

            # Parse numbered items from gaps
            lines = [
                re.sub(r'^\d+\.\s*', '', l.strip())
                for l in gaps.split("\n")
                if l.strip() and re.match(r'^\d+\.', l.strip())
            ]

            # ✅ Push ALL widget updates back to main thread via .after()
            def update_ui():
                # Update roadmap box
                roadmap_box.configure(state="normal")
                roadmap_box.delete("1.0", "end")
                render_markdown(roadmap_box, roadmap)
                roadmap_box.configure(state="disabled")

                # Rebuild checklist
                for widget in checklist_frame.winfo_children():
                    widget.destroy()

                if not lines:
                    ctk.CTkLabel(checklist_frame,
                                 text="No skills gap items found.",
                                 font=ctk.CTkFont(family="Nunito", size=12)).pack(pady=10)
                    return

                for item in lines[:15]:
                    var = ctk.BooleanVar()
                    cb = ctk.CTkCheckBox(
                        checklist_frame,
                        text=item,
                        variable=var,
                        font=ctk.CTkFont(family="Nunito", size=12)
                    )
                    cb.pack(anchor="w", pady=2, padx=10)

            frame.after(0, update_ui)

        threading.Thread(target=run, daemon=True).start()

    def go_back_to_step2():
        step3_frame.pack_forget()
        step2_frame.pack(fill="both", expand=True)

    ctk.CTkButton(step3_frame, text="← Back", command=go_back_to_step2,
                  font=ctk.CTkFont(family="Nunito", size=14)).pack(pady=10)

    # Show step 1 by default
    step1_frame.pack(fill="both", expand=True)

    return frame