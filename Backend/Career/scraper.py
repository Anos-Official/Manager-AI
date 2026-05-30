import requests
from config import SERPER_API_KEY

def search_canadian_jobs(job_title):
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json={"q": f"{job_title} jobs Canada 2025 salary demand site:jobbank.gc.ca OR site:indeed.ca OR site:glassdoor.ca"}
        )
        results = response.json().get("organic", [])
        context = ""
        for r in results[:5]:
            context += f"{r['title']}: {r['snippet']}\n"
        return context
    except Exception as e:
        return f"Search error: {e}"

def search_salary_canada(job_title):
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json={"q": f"{job_title} average salary Canada 2025 entry level senior"}
        )
        results = response.json().get("organic", [])
        context = ""
        for r in results[:5]:
            context += f"{r['title']}: {r['snippet']}\n"
        return context
    except Exception as e:
        return f"Search error: {e}"

def search_career_roadmap(job_title):
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json={"q": f"how to become {job_title} Canada skills required roadmap 2025"}
        )
        results = response.json().get("organic", [])
        context = ""
        for r in results[:5]:
            context += f"{r['title']}: {r['snippet']}\n"
        return context
    except Exception as e:
        return f"Search error: {e}"