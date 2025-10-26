#!/usr/bin/env python3
"""
Fetch publications from Google Scholar and output Nature-style citations
to _data/publications.yml.

Nature-ish format used:
Author, A. B., Author, C. D. & Author, E. F. Title. Journal Volume, pages (Year). DOI

Author listing rule:
- If <= 10 authors: list all
- If > 10 authors: list first 6, then "et al."

Requires:
  pip install scholarly PyYAML

Tip: run from the repo root:  python scripts/fetch_publications.py
"""

import os
import re
import yaml
from typing import List, Dict, Any
from scholarly import scholarly

SCHOLAR_ID = "hhKlTYYAAAAJ"  # <-- your Google Scholar ID
OUTPUT_PATH = "_data/publications.yml"

# --------------------------
# Helpers
# --------------------------

DOI_RE = re.compile(r"(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)")

def parse_authors(bib_author_field: Any) -> List[str]:
    """
    scholarly 'bib.author' can be a string like 'A Author and B Author'
    or a list. Normalize to a list of 'First Last' strings.
    """
    if isinstance(bib_author_field, list):
        raw = bib_author_field
    elif isinstance(bib_author_field, str):
        raw = [x.strip() for x in bib_author_field.replace(" and ", " , ").split(" , ") if x.strip()]
    else:
        return []
    return raw

def initials_from_first_names(first_parts: List[str]) -> str:
    """Turn ['Alice','B.','Carol'] -> 'A. B. C.'"""
    initials = []
    for p in first_parts:
        # strip punctuation, keep letters
        letters = re.sub(r"[^A-Za-z]", "", p)
        if letters:
            initials.append(letters[0].upper() + ".")
    return " ".join(initials)

def format_author(full_name: str) -> str:
    """
    Convert 'First Middle Last' or 'Last, First M.' -> 'Last, F. M.'
    Handles simple particles like 'van', 'de', 'da', etc. reasonably.
    """
    name = full_name.strip()
    # If already "Last, First ..." keep that split, else split normally
    if "," in name:
        last, first = [x.strip() for x in name.split(",", 1)]
        first_parts = first.split()
    else:
        parts = name.split()
        if len(parts) == 1:
            # Single token, treat as last name only
            return parts[0]
        # Heuristic: last name is the last token
        last = parts[-1]
        first_parts = parts[:-1]

    return f"{last}, {initials_from_first_names(first_parts)}".strip()

def format_author_list_nature(authors: List[str]) -> str:
    """
    Nature-like joining:
    - <=10 authors: A, B, C & D
    - >10 authors: first 6 then 'et al.'
    """
    formatted = [format_author(a) for a in authors]
    if len(formatted) == 0:
        return ""
    if len(formatted) > 10:
        formatted = formatted[:6] + ["et al."]
    if len(formatted) == 1:
        return formatted[0]
    # Oxford-ish with ampersand before last
    return ", ".join(formatted[:-1]) + " & " + formatted[-1]

def clean_pages(pages: str) -> str:
    """Replace hyphen with en dash if numeric range."""
    if not pages:
        return ""
    pages = pages.strip()
    if re.match(r"^\d+\s*-\s*\d+$", pages):
        return re.sub(r"\s*-\s*", "–", pages)
    return pages

def extract_doi(urls: List[str]) -> str:
    """Try to pull a DOI from any candidate URL."""
    for u in urls:
        if not u:
            continue
        m = DOI_RE.search(u)
        if m:
            return m.group(1)
    return ""

def nature_citation(bib: Dict[str, Any], doi: str) -> str:
    """
    Build the Nature-style string.
    Authors. Title. Journal Volume, pages (Year). DOI
    Only include pieces that exist; keep punctuation clean.
    """
    authors = format_author_list_nature(parse_authors(bib.get("author", [])))
    title = bib.get("title", "") or ""
    journal = (bib.get("journal") or bib.get("venue") or "").strip()
    volume = (bib.get("volume") or "").strip()
    pages = clean_pages(bib.get("pages", "") or "")
    year = str(bib.get("pub_year") or bib.get("year") or "").strip()

    parts = []
    if authors:
        parts.append(f"{authors}.")
    if title:
        parts.append(f"{title}.")
    jp = []
    if journal:
        jp.append(journal)
    if volume:
        jp.append(volume)
    if pages:
        # If we have volume and pages, prefer "Journal Volume, pages"
        if journal or volume:
            jp[-1] = f"{jp[-1]}," if jp else pages
            jp.append(pages)
        else:
            jp.append(pages)
    if year:
        # Append (Year).
        parts.append((" ".join(jp) if jp else "").strip() + (f" ({year})." if year else ""))
    else:
        if jp:
            parts.append(" ".join(jp) + ".")

    if doi:
        parts.append(f"https://doi.org/{doi}")

    # Clean extra spaces and stray punctuation
    citation = " ".join(p.strip() for p in parts if p.strip())
    citation = re.sub(r"\s+\.", ".", citation)
    citation = re.sub(r"\s+,", ",", citation)
    citation = re.sub(r"\(\s+(\d{4})\s+\)", r"(\1)", citation)
    return citation

# --------------------------
# Main
# --------------------------

def main():
    author = scholarly.search_author_id(SCHOLAR_ID)
    filled_author = scholarly.fill(author, sections=["publications"])

    out_items = []

    for pub in filled_author.get("publications", []):
        try:
            full = scholarly.fill(pub)  # fills bib + links
            bib = full.get("bib", {}) or {}

            # Collect possible URLs to hunt for a DOI
            candidate_urls = []
            for key in ("pub_url", "eprint_url", "url_scholarbib"):
                u = full.get(key)
                if u:
                    candidate_urls.append(u)

            doi = extract_doi(candidate_urls)

            # Build Nature-style citation
            citation = nature_citation(bib, doi)

            # Write a rich record so you can tweak downstream if needed
            item = {
                "title": bib.get("title", ""),
                "authors": parse_authors(bib.get("author", [])),
                "year": bib.get("pub_year") or bib.get("year"),
                "journal": bib.get("journal") or bib.get("venue"),
                "volume": bib.get("volume"),
                "issue": bib.get("number"),
                "pages": bib.get("pages"),
                "doi": doi,
                "url": full.get("pub_url") or full.get("eprint_url"),
                "citation": citation,
            }
            out_items.append(item)

        except Exception as e:
            print(f"Error processing publication: {e}")
            continue

    # Ensure _data exists; write YAML (stable key order)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        yaml.dump(out_items, f, allow_unicode=True, sort_keys=False)

    print(f"Saved {len(out_items)} publications to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()