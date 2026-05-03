from duckduckgo_search import DDGS

try:
    with DDGS() as ddgs:
        results = ddgs.text("best balanced healthy meals recipes", max_results=7)
        if results:
            print("Found:", [r['title'] for r in results])
        else:
            print("No results returned!")
except Exception as e:
    import traceback
    traceback.print_exc()
