def filter_jobs(jobs):
    results = []
    for job in jobs:
        # 1. Ort: Berlin
        location = job.get("location", "").lower()
        if "berlin" not in location:
            continue
        
        # 2. Job-Typ: Werkstudent
        job_types = [t.lower() for t in job.get("job_types", [])]
        is_werkstudent = any(
            "working student" in jt or "werkstudent" in jt 
            for jt in job_types
        ) or any("internship" in jt or "praktikum" in jt for jt in job_types)
        if not is_werkstudent:
            continue
        
        # 3. Fachbereich: Medien ODER Informatik
        text = " ".join([
            job.get("title", ""),
            " ".join(job.get("tags", [])),
            job.get("description", "")
        ]).lower()
        
        medien_keywords = [
            "medien", "media", "marketing", "kommunikation", 
            "communication", "design", "content", "social media",
            "journalismus", "journalism", "presse", "pr", 
            "öffentlichkeitsarbeit", "video", "film", "audio"
        ]
        informatik_keywords = [
            "informatik", "it", "software", "developer", "entwickler",
            "programmier", "python", "java", "javascript", "data",
            "engineering", "backend", "frontend", "web", "cloud",
            "devops", "ki", "ai", "machine learning", "datenbank"
        ]
        
        ist_medien = any(kw in text for kw in medien_keywords)
        ist_informatik = any(kw in text for kw in informatik_keywords)
        
        if not (ist_medien or ist_informatik):
            continue
        
        results.append(job)
    
    return results