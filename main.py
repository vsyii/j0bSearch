from arbeitnow import fetch_all_jobs as fetch_arbeitnow_jobs
from google import fetch_google_jobs
from normalizer import normalize_job
from filters import filter_jobs
from pdf_export import export_jobs_to_pdf


def main():
    # 1. Jobs von beiden APIs holen
    arbeitnow_raw = fetch_arbeitnow_jobs(max_pages=5)
    google_raw = fetch_google_jobs(
        query="Werkstudent Medien Informatik",
        location="Berlin, Germany",
        max_pages=3,
    )

    # 2. Normalisieren und zusammenführen
    all_jobs = []
    all_jobs.extend(normalize_job(j, "arbeitnow") for j in arbeitnow_raw)
    all_jobs.extend(normalize_job(j, "google") for j in google_raw)

    print(f"Insgesamt geladen: {len(all_jobs)} Jobs "
          f"({len(arbeitnow_raw)} Arbeitnow + {len(google_raw)} Google)")

    # 3. Filtern
    treffer = filter_jobs(all_jobs)
    print(f"Nach Filterung: {len(treffer)} Treffer")

    # 4. PDF erstellen
    if treffer:
        pfad = export_jobs_to_pdf(treffer, "werkstudent_berlin.pdf")
        print(f"PDF gespeichert: {pfad}")
    else:
        print("Keine Treffer – kein PDF erstellt.")

if __name__ == "__main__":
    main()