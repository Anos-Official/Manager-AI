import os
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def search_web(query):
    response = requests.get(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": os.getenv("SERPER_API_KEY")},
        json={"q": query}
    )
    results = response.json()["organic"]
    # extract top 3 results as text
    context = ""
    for r in results[:3]:
        context += f"{r['title']}: {r['snippet']}\n"
    return context

def ask_ai(prompt):
    context = search_web(prompt)
    full_prompt = f"{prompt}\n\nCurrent information:\n{context}"
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=1
    )
    return response.choices[0].message.content