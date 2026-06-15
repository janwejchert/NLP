"""Build the submission PDFs from the Markdown sources.

Produces, in ``docs/report/pdf/``:

* ``ATC_Readback_Verifier_Technical_Report.pdf`` — the technical report, with the
  full field review, full failure-mode analysis, and full "Use of AI tools" as
  appendices, so the report is self-contained.
* ``ATC_Readback_Verifier_Executive_Summary.pdf`` — the one-page non-technical summary.
* ``ATC_Readback_Verifier_Individual_Reflections.pdf`` — the six reflections, one per page-group.

The slide deck is built separately by ``build_slides.sh`` (Marp).

Pipeline: Markdown --(pandoc, gfm->html5)--> HTML fragment --(WeasyPrint)--> PDF.
WeasyPrint is used because it renders Unicode (box-drawing diagrams, arrows) and
tables cleanly with full CSS control. Run from anywhere:

    python docs/report/build_pdfs.py
"""

from __future__ import annotations

import re
import subprocess
from datetime import date
from pathlib import Path

from weasyprint import HTML

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE / "pdf"
TODAY = date.today().strftime("%B %Y")

# --------------------------------------------------------------------------- #
# Styling
# --------------------------------------------------------------------------- #
CSS = """
@page {
  size: A4;
  margin: 20mm 18mm 18mm 18mm;
  @bottom-center { content: counter(page) " / " counter(pages);
                   font-family: 'Helvetica Neue', Arial, sans-serif;
                   font-size: 8pt; color: #8a96a3; }
}
@page :first { @bottom-center { content: ""; } }

html { font-size: 10.5pt; }
body {
  font-family: Georgia, 'Times New Roman', serif;
  color: #1b1f24; line-height: 1.5; hyphens: auto;
}
h1, h2, h3, h4 {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: #0b3d5c; line-height: 1.25; font-weight: 700;
}
h1 { font-size: 18pt; margin: 0 0 .4em; padding-bottom: .25em;
     border-bottom: 2px solid #0b3d5c; break-before: page; }
h1.first { break-before: avoid; }
h2 { font-size: 13.5pt; margin: 1.3em 0 .45em;
     border-bottom: 1px solid #d7dee6; padding-bottom: .15em; }
h3 { font-size: 11.5pt; margin: 1.05em 0 .35em; color: #16557e; }
h4 { font-size: 10.5pt; margin: .9em 0 .3em; color: #16557e; }
p  { margin: 0 0 .65em; }
a  { color: #0b5e8a; text-decoration: none; }
strong { color: #11161c; }
ul, ol { margin: 0 0 .65em; padding-left: 1.4em; }
li { margin: .12em 0; }

table { border-collapse: collapse; width: 100%; margin: .6em 0 1em;
        font-size: 9.3pt; break-inside: avoid; }
th { background: #0b3d5c; color: #fff; text-align: left;
     padding: 6px 9px; font-family: 'Helvetica Neue', Arial, sans-serif;
     font-weight: 600; font-size: 8.8pt; }
td { padding: 5px 9px; border-bottom: 1px solid #dde3ea; vertical-align: top; }
tr:nth-child(even) td { background: #f4f7fa; }

pre { background: #f6f8fa; border: 1px solid #dfe5ec; border-radius: 5px;
      padding: 10px 12px; font-family: Menlo, 'DejaVu Sans Mono', monospace;
      font-size: 8.4pt; line-height: 1.35; white-space: pre; overflow: hidden;
      break-inside: avoid; color: #243240; }
code { font-family: Menlo, 'DejaVu Sans Mono', monospace; font-size: 9pt;
       background: #eef2f6; padding: .5px 4px; border-radius: 3px; color: #29445a; }
pre code { background: none; padding: 0; font-size: inherit; }

blockquote { margin: .6em 0; padding: .35em 0 .35em 14px;
             border-left: 3px solid #9bb4c6; color: #46535f; background: #f7f9fb; }
hr { border: 0; border-top: 1px solid #d7dee6; margin: 1.4em 0; }
em { color: #36424d; }

/* ---- title page ---- */
.title-page { break-after: page; padding-top: 32mm; text-align: center; }
.title-page .eyebrow { font-family: 'Helvetica Neue', Arial, sans-serif;
  letter-spacing: .22em; text-transform: uppercase; font-size: 9.5pt;
  color: #0b5e8a; margin-bottom: 20mm; }
.title-page h1 { font-size: 30pt; border: 0; break-before: avoid;
  margin: 0 0 .15em; color: #0b3d5c; }
.title-page .doctype { font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 15pt; color: #16557e; font-weight: 600; letter-spacing: .04em; }
.title-page .tagline { font-style: italic; color: #46535f; font-size: 11.5pt;
  max-width: 130mm; margin: 8mm auto 0; line-height: 1.5; }
.title-page .meta { margin-top: 26mm; font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 10pt; color: #2c3742; line-height: 1.9; }
.title-page .meta .k { color: #8a96a3; letter-spacing: .12em; text-transform: uppercase;
  font-size: 8pt; }
.title-page .scope { margin-top: 14mm; font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 9pt; color: #8a96a3; }

/* compact one-pager (exec summary) */
.compact body, body.compact { font-size: 10.5pt; }
"""

# Extra rules injected for the one-page executive summary so it fits a single page.
COMPACT_CSS = """
@page { margin: 13mm 18mm 12mm 18mm; }
body { line-height: 1.4; }
h2 { margin: .7em 0 .3em; font-size: 12.5pt; }
p { margin: 0 0 .5em; }
"""


def sh(cmd: list[str], **kw) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw).stdout


def strip_disclaimers(md: str) -> str:
    """Remove the team-internal '_Draft ..._' note lines from a source file."""
    out = []
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("_Draft") and s.endswith("_"):
            continue
        if s.startswith("_") and "before submission" in s:
            continue
        out.append(line)
    # collapse leading blank lines
    text = "\n".join(out)
    return re.sub(r"\A\n+", "", text)


def md_fragment(md: str) -> str:
    """Markdown -> HTML fragment via pandoc (GitHub-flavoured, with tables)."""
    return sh(["pandoc", "-f", "gfm", "-t", "html5"], input=md)


def first_h1(html: str) -> str:
    """Tag the first <h1> with class 'first' so it doesn't force a page break."""
    return re.sub(r"<h1(\s|>)", r'<h1 class="first"\1', html, count=1)


def render(out_name: str, body_html: str, body_class: str = "", extra_css: str = "") -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    doc = (
        f"<!doctype html><html><head><meta charset='utf-8'>"
        f"<style>{CSS}{extra_css}</style></head>"
        f"<body class='{body_class}'>{body_html}</body></html>"
    )
    out_path = OUT / out_name
    HTML(string=doc, base_url=str(ROOT)).write_pdf(str(out_path))
    print(f"  wrote {out_path.relative_to(ROOT)}")
    return out_path


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def title_page(eyebrow: str, title: str, doctype: str, tagline: str,
               scope: str = "Proof of concept — not operational software.") -> str:
    return f"""
    <div class="title-page">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{title}</h1>
      <div class="doctype">{doctype}</div>
      <div class="tagline">{tagline}</div>
      <div class="meta">
        <div><span class="k">Team</span><br>Jan · Vlad · Felipe · Alberto · Kishan · Yi</div>
        <div style="margin-top:6mm"><span class="k">Repository</span><br>github.com/janwejchert/NLP</div>
        <div style="margin-top:6mm"><span class="k">Date</span><br>{TODAY}</div>
      </div>
      <div class="scope">{scope}</div>
    </div>
    """


# --------------------------------------------------------------------------- #
# 1. Technical report (self-contained, with appendices)
# --------------------------------------------------------------------------- #
def build_technical_report() -> Path:
    parts: list[str] = []
    parts.append(title_page(
        "NLP Group Project · Option 1 — Application Development",
        "ATC Readback Verifier",
        "Technical Report",
        "A hybrid system that verifies a pilot read-back against a controller "
        "instruction — an LLM extracts structured fields, deterministic Python "
        "judges every discrepancy.",
    ))

    body = first_h1(md_fragment(strip_disclaimers(read("docs/report/technical_report.md"))))
    parts.append(body)

    appendices = [
        ("Appendix A — Field Review (full, with references)", "docs/report/field_review.md"),
        ("Appendix B — Failure-Mode Analysis (full)", "docs/report/failure_analysis.md"),
        ("Appendix C — Use of AI Tools (full)", "docs/report/use_of_ai_tools.md"),
    ]
    for heading, rel in appendices:
        src = strip_disclaimers(read(rel))
        # Drop a redundant leading top-level heading; the appendix H1 replaces it.
        src = re.sub(r"\A#{1,2} .*\n", "", src).lstrip("\n")
        parts.append(md_fragment(f"# {heading}\n\n") + md_fragment(src))

    return render("ATC_Readback_Verifier_Technical_Report.pdf", "".join(parts))


# --------------------------------------------------------------------------- #
# 2. Executive summary (one page)
# --------------------------------------------------------------------------- #
def build_executive_summary() -> Path:
    body = first_h1(md_fragment(strip_disclaimers(read("docs/report/executive_summary.md"))))
    header = (
        "<div style='font-family:Helvetica Neue,Arial,sans-serif;letter-spacing:.18em;"
        "text-transform:uppercase;font-size:8.5pt;color:#0b5e8a;margin-bottom:2mm'>"
        "ATC Readback Verifier · NLP Group Project (Option 1) · One-page summary</div>"
    )
    return render("ATC_Readback_Verifier_Executive_Summary.pdf", header + body,
                  "compact", extra_css=COMPACT_CSS)


# --------------------------------------------------------------------------- #
# 3. Individual reflections (one combined PDF)
# --------------------------------------------------------------------------- #
def build_reflections() -> Path | None:
    refl_dir = ROOT / "docs" / "reflections"
    order = ["jan", "vlad", "felipe", "alberto", "kishan", "yi"]
    parts = [title_page(
        "NLP Group Project · Option 1 — Application Development",
        "ATC Readback Verifier",
        "Individual Reflections",
        "One reflection per team member, as required by the assignment.",
        scope="",
    )]
    found = False
    for i, name in enumerate(order):
        f = refl_dir / f"{name}.md"
        if not f.exists():
            continue
        md = strip_disclaimers(f.read_text(encoding="utf-8"))
        html = md_fragment(md)
        if not found:
            html = first_h1(html)  # first one right after title page
        else:
            # force a page break before each subsequent reflection
            html = re.sub(r"<h1", "<h1", html, count=1)
        parts.append(html)
        found = True
    if not found:
        print("  (no reflections found yet — skipping)")
        return None
    return render("ATC_Readback_Verifier_Individual_Reflections.pdf", "".join(parts),
                  extra_css=COMPACT_CSS)


def main() -> None:
    print("Building submission PDFs ->", OUT.relative_to(ROOT))
    build_technical_report()
    build_executive_summary()
    build_reflections()
    print("Done.")


if __name__ == "__main__":
    main()
