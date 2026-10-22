import time
import requests

BASE_URL = "https://www.arbeitnow.com/api/job-board-api"


def fetch_all_jobs(max_pages=5):
    all_jobs = []
    url, params = BASE_URL, {"page": 1}

    for page in range(1, max_pages + 1):
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            payload = resp.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Fehler bei Arbeitnow (Seite {page}): {e}")
            break

        jobs = payload.get("data", [])
        if not jobs:
            break
        all_jobs.extend(jobs)
        print(f"Arbeitnow Seite {page}: {len(jobs)} Jobs geladen")

        
        next_url = (payload.get("links") or {}).get("next")
        if not next_url:
            break
        url, params = next_url, None
        time.sleep(0.5)

    return all_jobs