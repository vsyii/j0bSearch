import re
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer,
)


def _safe(text):
    """Escaped Sonderzeichen, damit ReportLab nicht crasht."""
    return escape(str(text or ""))


def _styles():
    base = getSampleStyleSheet()
    return {
        "base": base["Normal"],
        "title": ParagraphStyle("T", parent=base["Title"], fontSize=18,
                                spaceAfter=6, textColor=colors.HexColor("#1a1a1a")),
        "subtitle": ParagraphStyle("S", parent=base["Normal"], fontSize=10,
                                   textColor=colors.grey, spaceAfter=20,
                                   alignment=TA_LEFT),
        "job": ParagraphStyle("J", parent=base["Heading2"], fontSize=13,
                              spaceAfter=2, textColor=colors.HexColor("#0a3d62")),
        "meta": ParagraphStyle("M", parent=base["Normal"], fontSize=10,
                               spaceAfter=2, textColor=colors.HexColor("#333333")),
        "link": ParagraphStyle("L", parent=base["Normal"], fontSize=10,
                               spaceAfter=2, wordWrap="CJK"),  # lange URLs umbrechen
        "desc": ParagraphStyle("D", parent=base["Normal"], fontSize=9,
                               leading=12, textColor=colors.HexColor("#555555")),
    }


def _short(text, limit=300):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:limit].rsplit(" ", 1)[0] + "…" if len(text) > limit else text


def export_jobs_to_pdf(jobs, filename="werkstudent_jobs_berlin.pdf"):
    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="Werkstudent Jobs Berlin – Medien/IT",
    )
    st = _styles()

    # Neueste zuerst (Google-Jobs ohne Datum landen hinten)
    jobs = sorted(jobs, key=lambda j: j.get("created_at", 0), reverse=True)

    story = [
        Paragraph("Werkstudent Jobs – Berlin", st["title"]),
        Paragraph(
            f"Medien &amp; Informatik · {len(jobs)} Treffer · "
            f"Erstellt am {datetime.now():%d.%m.%Y %H:%M}",
            st["subtitle"],
        ),
    ]

    if not jobs:
        story.append(Paragraph("Keine Jobs gefunden.", st["base"]))
        doc.build(story)
        return filename

    for i, job in enumerate(jobs, 1):
        job_types = ", ".join(job.get("job_types") or []) or "–"
        tags = ", ".join((job.get("tags") or [])[:8]) or "–"
        block = [
            Paragraph(f"{i}. {_safe(job.get('title') or 'Ohne Titel')}", st["job"]),
            Paragraph(
                f"<b>Firma:</b> {_safe(job.get('company_name') or '–')} &nbsp;|&nbsp; "
                f"<b>Ort:</b> {_safe(job.get('location') or '–')} &nbsp;|&nbsp; "
                f"<b>Quelle:</b> {_safe(job.get('source') or '–')}",
                st["meta"],
            ),
            Paragraph(
                f"<b>Typ:</b> {_safe(job_types)} &nbsp;|&nbsp; <b>Tags:</b> {_safe(tags)}",
                st["meta"],
            ),
        ]

        url = job.get("url", "")
        if url:
            u = escape(url, {'"': "&quot;"})
            block.append(Paragraph(
                f'<b>Link:</b> <a href="{u}" color="#1a73e8">{u}</a>', st["link"]))

        desc = _short(job.get("description"))
        if desc:
            block += [Spacer(1, 4), Paragraph(_safe(desc), st["desc"])]

        block += [
            Spacer(1, 6),
            HRFlowable(width="100%", thickness=0.5,
                       color=colors.HexColor("#dddddd"), spaceAfter=12),
        ]
        story.append(KeepTogether(block))

    doc.build(story)
    return filename