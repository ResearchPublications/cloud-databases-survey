#!/usr/bin/env python3
"""
Download cited reference PDFs from cloud-db-metasurvey.bib into references/.

Strategy:
  1. Parse .bib file with regex
  2. Classify entries: skip (misc/books), arXiv, DOI-based, title-search fallback
  3. Download open-access PDFs via Semantic Scholar API and arXiv
  4. Save as references/{citation_key}.pdf
  5. Generate references/download_report.txt
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BIB_FILE = "cloud-db-metasurvey.bib"
OUTPUT_DIR = "references"
REPORT_FILE = os.path.join(OUTPUT_DIR, "download_report.txt")

SEMANTIC_SCHOLAR_PAPER = "https://api.semanticscholar.org/graph/v1/paper"
SS_FIELDS = "openAccessPdf,externalIds,title"

USER_AGENT = "CloudDB-MetaSurvey-RefDownloader/1.0 (academic research; polite crawl)"
PDF_TIMEOUT = 30  # seconds
API_DELAY = 1.1  # seconds between Semantic Scholar API calls

# Entries to skip: misc web resources and books (not single-file academic PDFs)
SKIP_KEYS = {
    # Misc / docs / reports / regulations
    "AmazonAurora2023",
    "GDPR2016",
    "gartner2024dbms",
    "IEA2024DataCenters",
    "IDC2024Cloud",
    # Books / textbooks
    "Kleppmann2017DesigningData",
    "Bernstein1987Concurrency",
    "Weikum2002Transactions",
    "Doan2012DataIntegration",
    "Ozsu2020DistributedDB",
    "Fuhrt2010CloudSecurity",
}

# ---------------------------------------------------------------------------
# BibTeX regex parser
# ---------------------------------------------------------------------------
# Matches @type{key, ... } allowing nested braces in field values
ENTRY_RE = re.compile(
    r"@(\w+)\s*\{\s*([^,]+)\s*,(.*?)\n\}",
    re.DOTALL,
)
FIELD_RE = re.compile(
    r"(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|\"((?:[^\"]|\\\")*)\"|(\d+))",
    re.DOTALL,
)


def parse_bib(path):
    """Parse a .bib file and return a list of entry dicts."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    entries = []
    for m in ENTRY_RE.finditer(text):
        entry_type = m.group(1).lower()
        key = m.group(2).strip()
        body = m.group(3)

        fields = {}
        for fm in FIELD_RE.finditer(body):
            fname = fm.group(1).lower()
            fval = fm.group(2) or fm.group(3) or fm.group(4) or ""
            # Clean up LaTeX artifacts
            fval = fval.strip()
            fval = re.sub(r"\s+", " ", fval)
            fields[fname] = fval

        entries.append(
            {
                "key": key,
                "type": entry_type,
                "doi": fields.get("doi", ""),
                "title": fields.get("title", ""),
                "journal": fields.get("journal", ""),
                "booktitle": fields.get("booktitle", ""),
                "howpublished": fields.get("howpublished", ""),
                "url": fields.get("url", ""),
                "year": fields.get("year", ""),
            }
        )
    return entries


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------
def classify_entries(entries):
    """Classify entries into skip / arxiv / doi / title_search buckets."""
    skip, arxiv, doi, title_search = [], [], [], []

    for e in entries:
        key = e["key"]

        # 1. Explicit skip list
        if key in SKIP_KEYS:
            skip.append((e, "in skip list (misc/book)"))
            continue

        # 2. arXiv bucket: journal field contains "arXiv"
        journal_combined = e["journal"] + " " + e.get("booktitle", "")
        if "arxiv" in journal_combined.lower():
            arxiv.append(e)
            continue

        # 3. DOI bucket
        if e["doi"]:
            doi.append(e)
            continue

        # 4. Title-search fallback
        if e["title"]:
            title_search.append(e)
            continue

        # Nothing to work with
        skip.append((e, "no DOI, no arXiv, no title"))

    return skip, arxiv, doi, title_search


def extract_arxiv_id(entry):
    """Extract arXiv ID from journal field like 'arXiv preprint arXiv:2312.17449'."""
    text = entry["journal"]
    # Pattern: arXiv:YYMM.NNNNN or arXiv:YYMM.NNNNNvN
    m = re.search(r"arXiv[:\s]+(\d{4}\.\d{4,5}(?:v\d+)?)", text, re.IGNORECASE)
    if m:
        return m.group(1)
    # Sometimes just the number after "arXiv preprint"
    m = re.search(r"(\d{4}\.\d{4,5}(?:v\d+)?)", text)
    if m:
        return m.group(1)
    return None


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------
def make_request(url, timeout=PDF_TIMEOUT):
    """Make an HTTP GET request with our user agent. Returns (data, content_type) or raises."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    resp = urllib.request.urlopen(req, timeout=timeout)
    return resp.read(), resp.headers.get("Content-Type", "")


def query_semantic_scholar(query_url):
    """Query Semantic Scholar API. Returns parsed JSON dict or None."""
    try:
        data, _ = make_request(query_url, timeout=15)
        return json.loads(data)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return None


def download_pdf(url, dest_path):
    """Download a PDF from url to dest_path. Returns True if valid PDF."""
    try:
        data, ctype = make_request(url, timeout=PDF_TIMEOUT)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
        return False, f"download error: {exc}"

    # Validate PDF header
    if not data[:5] == b"%PDF-":
        # Some servers return HTML error pages
        if b"<html" in data[:500].lower():
            return False, "received HTML instead of PDF"
        # Could be gzipped PDF or other encoding – still save if large enough
        if len(data) < 1000:
            return False, f"too small ({len(data)} bytes), likely not a PDF"

    with open(dest_path, "wb") as f:
        f.write(data)
    return True, "ok"


def try_semantic_scholar_download(ss_result, dest_path):
    """Given a Semantic Scholar paper result, try to download the PDF.
    Returns (success, source_description)."""
    if not ss_result:
        return False, "Semantic Scholar returned no result"

    # Try openAccessPdf first
    oa = ss_result.get("openAccessPdf")
    if oa and oa.get("url"):
        pdf_url = oa["url"]
        ok, msg = download_pdf(pdf_url, dest_path)
        if ok:
            return True, f"openAccessPdf: {pdf_url}"

    # Fallback: check if there's an arXiv ID in externalIds
    ext_ids = ss_result.get("externalIds") or {}
    arxiv_id = ext_ids.get("ArXiv")
    if arxiv_id:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        ok, msg = download_pdf(pdf_url, dest_path)
        if ok:
            return True, f"arXiv fallback: {pdf_url}"

    return False, "no open-access PDF available"


def clean_title_for_search(title):
    """Remove LaTeX commands and braces from title for API search."""
    title = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", title)  # \cmd{text} -> text
    title = re.sub(r"[{}]", "", title)
    title = re.sub(r"\\", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title


# ---------------------------------------------------------------------------
# Main download logic
# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Parsing {BIB_FILE}...")
    entries = parse_bib(BIB_FILE)
    print(f"  Found {len(entries)} bibliography entries.\n")

    skip_list, arxiv_list, doi_list, title_list = classify_entries(entries)
    print(f"  Skip:         {len(skip_list)}")
    print(f"  arXiv:        {len(arxiv_list)}")
    print(f"  DOI:          {len(doi_list)}")
    print(f"  Title search: {len(title_list)}")
    print()

    # Track results for report
    results = []  # list of (key, status, detail)

    # Record skipped entries
    for entry, reason in skip_list:
        results.append((entry["key"], "SKIPPED", reason))

    # --- arXiv downloads ---
    print("=" * 60)
    print("Downloading arXiv papers...")
    print("=" * 60)
    for entry in arxiv_list:
        key = entry["key"]
        dest = os.path.join(OUTPUT_DIR, f"{key}.pdf")

        if os.path.exists(dest):
            print(f"  [{key}] already exists, skipping.")
            results.append((key, "EXISTS", dest))
            continue

        arxiv_id = extract_arxiv_id(entry)
        if not arxiv_id:
            print(f"  [{key}] could not extract arXiv ID from: {entry['journal']}")
            results.append((key, "FAILED", "could not extract arXiv ID"))
            continue

        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        print(f"  [{key}] downloading {pdf_url} ...", end=" ", flush=True)

        ok, msg = download_pdf(pdf_url, dest)
        if ok:
            size_kb = os.path.getsize(dest) / 1024
            print(f"OK ({size_kb:.0f} KB)")
            results.append((key, "DOWNLOADED", pdf_url))
        else:
            print(f"FAILED: {msg}")
            results.append((key, "FAILED", f"arXiv download: {msg}"))

        time.sleep(0.5)  # Be polite to arXiv

    # --- DOI-based Semantic Scholar downloads ---
    print()
    print("=" * 60)
    print("Downloading DOI-based papers via Semantic Scholar...")
    print("=" * 60)
    for entry in doi_list:
        key = entry["key"]
        dest = os.path.join(OUTPUT_DIR, f"{key}.pdf")

        if os.path.exists(dest):
            print(f"  [{key}] already exists, skipping.")
            results.append((key, "EXISTS", dest))
            continue

        doi = entry["doi"]
        api_url = f"{SEMANTIC_SCHOLAR_PAPER}/DOI:{urllib.parse.quote(doi, safe='')}?fields={SS_FIELDS}"
        print(f"  [{key}] querying DOI:{doi} ...", end=" ", flush=True)

        ss_result = query_semantic_scholar(api_url)
        if ss_result:
            ok, detail = try_semantic_scholar_download(ss_result, dest)
            if ok:
                size_kb = os.path.getsize(dest) / 1024
                print(f"OK ({size_kb:.0f} KB) — {detail}")
                results.append((key, "DOWNLOADED", detail))
            else:
                print(f"no PDF: {detail}")
                results.append((key, "FAILED", detail))
        else:
            print("API returned no result")
            results.append((key, "FAILED", f"Semantic Scholar API returned nothing for DOI:{doi}"))

        time.sleep(API_DELAY)

    # --- Title-based Semantic Scholar fallback ---
    print()
    print("=" * 60)
    print("Downloading papers via title search (Semantic Scholar)...")
    print("=" * 60)
    for entry in title_list:
        key = entry["key"]
        dest = os.path.join(OUTPUT_DIR, f"{key}.pdf")

        if os.path.exists(dest):
            print(f"  [{key}] already exists, skipping.")
            results.append((key, "EXISTS", dest))
            continue

        clean_title = clean_title_for_search(entry["title"])
        if not clean_title:
            print(f"  [{key}] no usable title")
            results.append((key, "FAILED", "empty title after cleaning"))
            continue

        query = urllib.parse.quote(clean_title)
        api_url = f"{SEMANTIC_SCHOLAR_PAPER}/search?query={query}&fields={SS_FIELDS}&limit=1"
        print(f"  [{key}] searching: {clean_title[:60]}...", end=" ", flush=True)

        ss_result = query_semantic_scholar(api_url)
        if ss_result and ss_result.get("data") and len(ss_result["data"]) > 0:
            paper = ss_result["data"][0]
            ok, detail = try_semantic_scholar_download(paper, dest)
            if ok:
                size_kb = os.path.getsize(dest) / 1024
                print(f"OK ({size_kb:.0f} KB) — {detail}")
                results.append((key, "DOWNLOADED", detail))
            else:
                print(f"no PDF: {detail}")
                results.append((key, "FAILED", detail))
        else:
            print("no search results")
            results.append((key, "FAILED", "Semantic Scholar title search returned no results"))

        time.sleep(API_DELAY)

    # --- Generate report ---
    print()
    print("=" * 60)
    print("Generating download report...")
    print("=" * 60)

    downloaded = sum(1 for _, s, _ in results if s == "DOWNLOADED")
    existed = sum(1 for _, s, _ in results if s == "EXISTS")
    failed = sum(1 for _, s, _ in results if s == "FAILED")
    skipped = sum(1 for _, s, _ in results if s == "SKIPPED")

    report_lines = [
        "=" * 70,
        "DOWNLOAD REPORT — Cloud DB Meta-Survey References",
        "=" * 70,
        "",
        f"Total entries:   {len(entries)}",
        f"Downloaded:      {downloaded}",
        f"Already existed: {existed}",
        f"Failed:          {failed}",
        f"Skipped:         {skipped}",
        "",
        "-" * 70,
        f"{'KEY':<35} {'STATUS':<12} DETAIL",
        "-" * 70,
    ]

    for key, status, detail in sorted(results, key=lambda x: x[0]):
        report_lines.append(f"{key:<35} {status:<12} {detail}")

    report_lines.append("")
    report_lines.append("-" * 70)

    report_text = "\n".join(report_lines) + "\n"

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\nReport written to {REPORT_FILE}")
    print(f"\nSummary: {downloaded} downloaded, {existed} existed, {failed} failed, {skipped} skipped (of {len(entries)} total)")

    # Validate downloaded PDFs
    print("\nValidating downloaded PDFs...")
    invalid_count = 0
    for fname in os.listdir(OUTPUT_DIR):
        if not fname.endswith(".pdf"):
            continue
        fpath = os.path.join(OUTPUT_DIR, fname)
        with open(fpath, "rb") as f:
            header = f.read(5)
        if header != b"%PDF-":
            print(f"  WARNING: {fname} does not have a valid PDF header")
            invalid_count += 1
    if invalid_count == 0:
        print("  All PDFs have valid headers.")
    else:
        print(f"  {invalid_count} file(s) may not be valid PDFs.")


if __name__ == "__main__":
    main()
