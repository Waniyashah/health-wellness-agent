from duckduckgo_search import DDGS
import json

def test():
    with DDGS() as ddgs:
        results = ddgs.text("best vegetarian meals recipes", max_results=7)
        for r in results:
            print(r['title'])

if __name__ == "__main__":
    test()
