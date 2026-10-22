def normalize_job(job, source):
    
    if source == "arbeitnow":
        return {
            "title": job.get("title", ""),
            "company_name": job.get("company_name", ""),
            "location": job.get("location", ""),
            "url": job.get("url", ""),
            "description": job.get("description", ""),
            "tags": job.get("tags", []),
            "job_types": job.get("job_types", []),
            "remote": job.get("remote", False),
            "created_at": job.get("created_at", 0),
            "source": "Arbeitnow",
        }
    elif source == "google":
        return {
            "title": job.get("title", ""),
            "company_name": job.get("company_name", ""),
            "location": job.get("location", ""),
            "url": job.get("share_link", job.get("link", "")),
            "description": job.get("description", ""),
            "tags": [],  # Google Jobs liefert keine Tags
            "job_types": [],  # Keine strukturierten Job-Typen
            "remote": "remote" in job.get("location", "").lower()
                      or "remote" in job.get("description", "").lower(),
            "created_at": 0,  # Google liefert kein Erstellungsdatum
            "source": "Google Jobs",
        }
    return job