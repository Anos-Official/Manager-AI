from Backend.Career.career_ai import get_career_suggestions

result = get_career_suggestions(
    interests="coding, building apps",
    skills="Python, Lua basics",
    education="high school"
)
print(result)