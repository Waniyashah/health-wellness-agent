import json
from duckduckgo_search import DDGS

try:
    with DDGS() as ddgs:
        results = ddgs.text("best balanced healthy meals recipes", max_results=7)
        meals = [r['title'] for r in results] if results else []
        with open('meals.json', 'w', encoding='utf-8') as f:
            json.dump(meals, f)
except Exception as e:
    with open('meals.json', 'w', encoding='utf-8') as f:
        json.dump({"error": str(e)}, f)
