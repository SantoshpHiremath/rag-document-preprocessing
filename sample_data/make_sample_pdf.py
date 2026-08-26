"""Generates a small multi-page sample PDF used as real test fixture data.

Run once to produce sample_data/sample_report.pdf. This is checked into
the repo so tests don't depend on regenerating it, but the generator is
kept for reproducibility.
"""

import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUT_PATH = os.path.join(os.path.dirname(__file__), "sample_report.pdf")


def make_pdf(path: str = OUT_PATH) -> None:
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    # Page 1
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "Quarterly Maintenance Report")
    c.setFont("Helvetica", 11)
    c.drawString(72, height - 100, "Section 1: Track Inspection Summary")
    c.drawString(72, height - 120, "A total of 42 track segments were inspected during Q2.")
    c.drawString(72, height - 140, "3 segments were flagged for follow-up repair work.")
    c.showPage()

    # Page 2
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, height - 72, "Section 2: Sensor Readings")
    c.setFont("Helvetica", 11)
    c.drawString(72, height - 100, "Average rail temperature: 28.4 degrees C")
    c.drawString(72, height - 120, "Maximum vibration reading: 4.7 mm/s")
    c.drawString(72, height - 140, "No anomalies exceeded safety thresholds this quarter.")
    c.showPage()

    # Page 3
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, height - 72, "Section 3: Recommendations")
    c.setFont("Helvetica", 11)
    c.drawString(72, height - 100, "Schedule repair crews for the 3 flagged segments within 30 days.")
    c.drawString(72, height - 120, "Recalibrate vibration sensors on line B before next quarter.")
    c.showPage()

    c.save()


if __name__ == "__main__":
    make_pdf()
    print(f"wrote {OUT_PATH}")
