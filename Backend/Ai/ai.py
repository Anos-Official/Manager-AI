import os
import requests
import re
from config import GROQ_API_KEY, SERPER_API_KEY
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

def search_web(query):
    try:
        response = requests.post(
    "https://google.serper.dev/search",
    headers={
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
        },
    json={"q": query}
        )
        data = response.json()
        results = data.get("organic", [])
        context = ""
        for r in results[:3]:
            context += f"{r['title']}: {r['snippet']}\n"
        return context
    except Exception as e:
        print(f"search_web error: {e}")
        return ""

def needs_search(prompt):
    decision = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": "Reply only with 'yes' or 'no'. Does this question require current real world information from the internet to answer accurately?"},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    result = decision.choices[0].message.content
    result = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL).strip()
    print(f"needs_search: {result}")
    return result == "yes"

def ask_ai(prompt, system_prompt="You are Manager AI, a personal productivity assistant."):
    try:
        context = ""
        if needs_search(prompt):
            context = search_web(prompt)
        
        full_prompt = f"{prompt}\n\nCurrent information:\n{context}" if context else prompt
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
                ],
            temperature=1,
            max_completion_tokens=4096
        )
        content = response.choices[0].message.content
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
        return content
    except Exception as e:
        return f"AI unavailable: {e}"