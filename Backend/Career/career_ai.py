from Backend.Ai.ai import ask_ai
from Backend.Career.scraper import search_canadian_jobs, search_salary_canada, search_career_roadmap
from Backend.Career.resume import read_resume

CAREER_SYSTEM_PROMPT = """You are a Canadian career advisor for Manager AI.
You help users plan their careers specifically within the Canadian job market.
Always reference Canadian salaries in CAD, Canadian provinces, and Canadian specific resources.
Be specific, actionable, and realistic. Format responses clearly with headers and bullet points."""

def extract_profile_from_resume(resume_path):
    try:
        resume_text = read_resume(resume_path)
        prompt = f"""Extract the following from this resume and return as structured data:
        - Full name
        - Education level and field
        - List of technical skills
        - Work experience (job titles and duration)
        - Any certifications

        Resume:
        {resume_text}"""
        return ask_ai(prompt, system_prompt=CAREER_SYSTEM_PROMPT)
    except Exception as e:
        return f"Error extracting profile: {e}"

def get_career_suggestions(interests, skills, education):
    try:
        prompt = f"""Based on this profile, suggest 3-5 career paths:
        Interests: {interests}
        Current Skills: {skills}
        Education: {education}
        For each career show: job title, why it fits, average Canadian salary, demand level."""
        jobs_data = search_canadian_jobs(interests)
        return ask_ai(prompt + f"\n\nCurrent market data:\n{jobs_data}", system_prompt=CAREER_SYSTEM_PROMPT)
    except Exception as e:
        return f"Error getting suggestions: {e}"

def get_roadmap(career_goal, current_skills):
    try:
        prompt = f"""Create a detailed step by step roadmap to become a {career_goal} in Canada.
        Current skills: {current_skills}
        Include: skills to learn in order, certifications, experience needed, realistic timeline."""
        roadmap_data = search_career_roadmap(career_goal)
        return ask_ai(prompt + f"\n\nCurrent data:\n{roadmap_data}", system_prompt=CAREER_SYSTEM_PROMPT)
    except Exception as e:
        return f"Error getting roadmap: {e}"

def get_market_info(career_goal):
    try:
        prompt = f"""Provide Canadian job market info for {career_goal}:
        - Is it in demand? Which provinces?
        - Entry level vs senior salary ranges in CAD
        - Realistic timeline to first job
        - Top employers in Canada"""
        jobs_data = search_canadian_jobs(career_goal)
        salary_data = search_salary_canada(career_goal)
        return ask_ai(prompt + f"\n\nMarket data:\n{jobs_data}\nSalary data:\n{salary_data}", system_prompt=CAREER_SYSTEM_PROMPT)
    except Exception as e:
        return f"Error getting market info: {e}"

def get_skills_gap(career_goal, current_skills, resume_path=None):
    try:
        profile = ""
        if resume_path:
            profile = f"\n\nResume data:\n{read_resume(resume_path)}"
        prompt = f"""Skills gap analysis for someone who wants to be a {career_goal} in Canada.
        They currently know: {current_skills}
        Show: what skills are missing, priority order to learn them, estimated time per skill, 
        recommended resources for each skill.{profile}"""
        roadmap_data = search_career_roadmap(career_goal)
        return ask_ai(prompt + f"\n\nIndustry data:\n{roadmap_data}", system_prompt=CAREER_SYSTEM_PROMPT)
    except Exception as e:
        return f"Error getting skills gap: {e}"