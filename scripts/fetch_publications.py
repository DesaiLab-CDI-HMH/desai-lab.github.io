#!/usr/bin/env python3
"""
Enrich _data/publications.yml with:
  - year: int (derived if missing)
  - citation_nature: str (Nature-style: Authors. Title. Journal Volume(issue), pages (Year). doi:DOI)
Also sorts entries (newest first) if --sort is provided.

INPUT SHAPE (flexible):
Each publication can have keys like:
  title, authors, journal, volume, issue, pages, year, published, date, doi, url, pmid

'authors' may be:
  - list of dicts: [{'family':'Desai','given':'Jigar P.'}, ...]
  - list of strings: ['Jigar P. Desai', 'Jane Q. Doe', ...] OR ['Desai, Jigar P.', 'Doe, Jane Q.']
  - single string with separators: 'Desai, Jigar P.; Doe, Jane Q.'

USAGE:
  python3 scripts/fetch_publications.py \
      --in _data/publications.yml \
      --out _data/publications.yml \
      --sort
"""

import argparse
import copy
import datetime as dt
import os
import re
import sys
from typing import List, Dict, Any

try:
    import yaml  # PyYAML
except ImportError:
    sys.stderr.write("ERROR: PyYAML not installed. Try: pip install pyyaml\n")
    sys.exit(1)


# --------------------------- Helpers --------------------------------- #

def _strip(s: Any) -> str:
    return s.strip() if isinstance(s, str) else s


def parse_author_name(name: str):
    """
    Return (family, given) from a free-form author string.
    Tries 'Last, First Middle' first; falls back to last token as family.
    """
    name = name.strip()
    if "," in name:
        parts = [p.strip() for p in name.split(",", 1)]
        family = parts[0]
        given = parts[1] if len(parts) > 1 else ""
        return family, given
    # No comma form: assume last token is family, rest is given
    tokens = name.split()
    if len(tokens) == 1:
        return tokens[0], ""
    family = tokens[-1]
    given = " ".join(tokens[:-1])
    return family, given


def initials(given: str) -> str:
    """
    Convert 'Jigar P.' or 'Jane Q' -> 'J.P.' or 'J.Q.'
    Keep hyphenated names: 'Jean-Pierre' -> 'J.-P.'
    """
    if not given:
        return ""
    # Remove stray punctuation at ends
    given = given.strip()
    # Handle hyphens
    parts = re.split(r"\s+", given.replace("–", "-"))
    out = []
    for p in parts:
        for chunk in p.split("-"):
            if chunk:
                out.append(chunk[0].upper() + ".")
        if "-" in p:
            out.append("-")
    # Re-join hyphenated initials properly
    joined = []
    skip_next = False
    for i, tok in enumerate(out):
        if tok == "-":
            # join last and next with hyphen
            if joined:
                joined[-1] = joined[-1] + "-"
            skip_next = False
        else:
            joined.append(tok)
    return "".join(joined)


def format_authors_nature(author_objs: List[Dict[str, str]]) -> str:
    """
    Nature-ish author formatting:
      - "Family F.I., Family F.I., Family F.I. & Family F.I."
      - If > 6 authors, list first 6 then 'et al.'
    """
    MAX_LIST = 6
    formatted = []
    for a in author_objs:
        family = a.get("family") or a.get("last") or a.get("surname") or ""
        given  = a.get("given")  or a.get("first") or a.get("forename") or ""
        family = family.strip()
        gi = initials(given)
        if family and gi:
            formatted.append(f"{family} {gi}")
        elif family:
            formatted.append(family)
        else:
            # fallback if weird record
            nm = (given or "").strip()
            formatted.append(nm if nm else "Unknown")
    if len(formatted) == 0:
        return ""
    if len(formatted) > MAX_LIST:
        formatted = formatted[:MAX_LIST] + ["et al."]
    if len(formatted) == 1:
        return formatted[0]
    if formatted[-1] == "et al.":
        return ", ".join(formatted[:-1]) + ", et al."
    # Oxford style ampersand before last
    return ", ".join(formatted[:-1]) + " & " + formatted[-1]


def normalize_authors(raw) -> List[Dict[str, str]]:
    """
    Normalize 'authors' into list of dicts with 'family' and 'given' keys.
    """
    if raw is None:
        return []
    # If already in dict form
    if isinstance(raw, list) and len(raw) > 0 and isinstance(raw[0], dict):
        # Ensure keys
        norm = []
        for a in raw:
            family = a.get("family") or a.get("last") or a.get("surname") or ""
            given  = a.get("given")  or a.get("first") or a.get("forename") or ""
            norm.append({"family": family.strip(), "given": given.strip()})
        return norm

    # If list of strings
    if isinstance(raw, list) and len(raw) > 0 and isinstance(raw[0], str):
        norm = []
        for s in raw:
            fam, giv = parse_author_name(s)
            norm.append({"family": fam, "given": giv})
        return norm

    # Single string with separators
    if isinstance(raw, str):
        # split on ; or and or ,
        cand = re.split(r";|\band\b", raw)
        if len(cand) == 1:
            cand = raw.split(",")
            # if it looked like "Last, First, Last2, First2" pair up
            if len(cand) % 2 == 0 and len(cand) > 2:
                pairs = [", ".join(cand[i:i+2]).strip() for i in range(0, len(cand), 2)]
                return normalize_authors(pairs)
        names = [c.strip() for c in cand if c.strip()]
        return normalize_authors(names)

    return []


def extract_year(rec: Dict[str, Any]) -> int:
    """
    Prefer explicit 'year'. Else derive from 'published' or 'date' (YYYY or YYYY-MM or YYYY-MM-DD).
    """
    for key in ("year", "Year"):
        if key in rec:
            try:
                return int(str(rec[key])[:4])
            except Exception:
                pass
    for key in ("published", "date", "issued", "pub_date"):
        val = rec.get(key)
        if isinstance(val, str):
            m = re.match(r"(\d{4})", val.strip())
            if m:
                return int(m.group(1))
        if isinstance(val, dict):
            # crossref-like {"date-parts":[[YYYY, M, D]]}
            dp = val.get("date-parts") or val.get("date_parts")
            if isinstance(dp, list) and dp and isinstance(dp[0], list) and dp[0]:
                try:
                    return int(dp[0][0])
                except Exception:
                    pass
    # As a last resort, try pages like '123-129 (2021)'
    for key in ("pages", "citation", "title", "journal"):
        v = rec.get(key)
        if isinstance(v, str):
            m = re.search(r"\((\d{4})\)", v)
            if m:
                return int(m.group(1))
    return dt.datetime.now().year


def build_citation_nature(rec: Dict[str, Any]) -> str:
    """
    Build Nature-style citation string:
      Authors. Title. Journal Volume(issue), pages (Year). doi:DOI
    Only include parts that exist.
    """
    authors = normalize_authors(rec.get("authors"))
    authors_str = format_authors_nature(authors)
    title  = (rec.get("title") or rec.get("Title") or "").strip()
    journal = (rec.get("journal") or rec.get("container-title") or rec.get("container_title") or "").strip()
    volume  = _strip(rec.get("volume"))
    issue   = _strip(rec.get("issue"))
    pages   = _strip(rec.get("pages") or rec.get("page"))
    year    = extract_year(rec)
    doi     = (rec.get("doi") or rec.get("DOI") or "").strip()
    url     = (rec.get("url") or rec.get("URL") or "").strip()

    # Compose journal part
    vol_issue = ""
    if volume and issue:
        vol_issue = f"{volume}({issue})"
    elif volume:
        vol_issue = f"{volume}"

    jvp = journal
    if vol_issue:
        jvp = f"{jvp} {vol_issue}"
    if pages:
        if vol_issue:
            jvp = f"{jvp}, {pages}"
        else:
            jvp = f"{jvp} {pages}"

    # Compose DOI/URL part
    tail = ""
    if doi:
        tail = f" doi:{doi}"
    elif url:
        tail = f" {url}"

    pieces = []
    if authors_str:
        pieces.append(f"{authors_str}.")
    if title:
        pieces.append(f"{title}.")
    if jvp:
        pieces.append(f"{jvp} ({year}).")
    else:
        pieces.append(f"({year}).")
    if tail:
        pieces.append(tail)

    return " ".join(pieces).replace("  ", " ").strip()


def _sort_key(rec):
    # Newest first: (-year, then title)
    y = extract_year(rec)
    title = (rec.get("title") or "").lower()
    return (-int(y), title)


# --------------------------- Main ------------------------------------ #

def main():
    ap = argparse.ArgumentParser(description="Enrich publications YAML with Nature-style citations and year.")
    ap.add_argument("--in", dest="infile", default="_data/publications.yml", help="Input YAML (default: _data/publications.yml)")
    ap.add_argument("--out", dest="outfile", default="_data/publications.yml", help="Output YAML (default: _data/publications.yml)")
    ap.add_argument("--sort", action="store_true", help="Sort newest first before writing")
    ap.add_argument("--no-backup", action="store_true", help="Do not create a timestamped backup of the output file")
    args = ap.parse_args()

    if not os.path.exists(args.infile):
        sys.stderr.write(f"ERROR: Input YAML not found: {args.infile}\n")
        sys.exit(1)

    with open(args.infile, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or []

    if not isinstance(data, list):
        sys.stderr.write("ERROR: Expected a YAML list of publications.\n")
        sys.exit(1)

    out_items = []
    for rec in data:
        item = copy.deepcopy(rec) if isinstance(rec, dict) else {}
        # Ensure year
        item["year"] = extract_year(item)
        # Build Nature citation
        item["citation_nature"] = build_citation_nature(item)
        out_items.append(item)

    if args.sort:
        out_items.sort(key=_sort_key)

    # Backup
    if not args.no_backup and os.path.exists(args.outfile):
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = f"{args.outfile}.{stamp}.bak"
        try:
            with open(args.outfile, "r", encoding="utf-8") as f_in, open(bak, "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())
            print(f"Backup written to {bak}")
        except Exception as e:
            sys.stderr.write(f"WARNING: Could not write backup: {e}\n")

    # Write
    os.makedirs(os.path.dirname(args.outfile) or ".", exist_ok=True)
    with open(args.outfile, "w", encoding="utf-8") as f:
        yaml.safe_dump(out_items, f, sort_keys=False, allow_unicode=True)
    print(f"Wrote {len(out_items)} records -> {args.outfile}")


if __name__ == "__main__":
    main()