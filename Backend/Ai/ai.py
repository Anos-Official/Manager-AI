import os
import requests
import re
from config import GROQ_API_KEY, SERPER_API_KEY
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

def search_web(query):
    response = requests.get(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": SERPER_API_KEY},
        json={"q": query}
    )
    results = response.json()["organic"]
    # extract top 3 results as text
    context = ""
    for r in results[:3]:
        context += f"{r['title']}: {r['snippet']}\n"
    return context

def needs_search(prompt):
    decision = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": "Reply only with 'yes' or 'no'. Does this question require current real world information from the internet to answer accurately?"},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    result = decision.choices[0].message.content.strip().lower()
    print(f"needs_search: {result}")  # debug
    return result == "yes"

def ask_ai(prompt):
    try:
        context = ""
        if needs_search(prompt):
            context = search_web(prompt)
        
        full_prompt = f"{prompt}\n\nCurrent information:\n{context}" if context else prompt
        
        response = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=1,
            max_completion_tokens=4096
        )
        content = response.choices[0].message.content
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
        return content
    except Exception as e:
        return f"AI unavailable: {e}"