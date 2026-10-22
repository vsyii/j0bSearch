import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()  #

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
BASE_URL = "https://serpapi.com/search"

def fetch_google_jobs(query, location, max_pages=3):
  
    all_jobs = []
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "gl": "de",   # Land: Deutschland
        "hl": "de",   # Sprache: Deutsch
        "google_domain": "google.de",  # Empfohlen für bessere lokale Ergebnisse
    }

    next_page_token = None
    for page in range(max_pages):
        if next_page_token:
            params["next_page_token"] = next_page_token

        try:
            resp = requests.get(BASE_URL, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei SerpApi (Seite {page + 1}): {e}")
            break

        jobs = data.get("jobs_results", [])
        if not jobs:
            break  # Keine weiteren Ergebnisse

        all_jobs.extend(jobs)
        print(f"SerpApi Seite {page + 1}: {len(jobs)} Jobs geladen")

        
        pagination = data.get("serpapi_pagination", {})
        next_page_token = pagination.get("next_page_token")
        if not next_page_token:
            break  # Keine weitere Seite verfügbar

        time.sleep(0.5)  # Höflichkeitspause

    return all_jobs