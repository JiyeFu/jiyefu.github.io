from scholarly import scholarly
import json
from datetime import datetime, timezone
from pathlib import Path
import os
import re


REPO_ROOT = Path(__file__).resolve().parents[1]
OVERRIDES_PATH = REPO_ROOT / "_data" / "scholar_publication_overrides.json"


def load_overrides():
    if OVERRIDES_PATH.exists():
        with OVERRIDES_PATH.open("r", encoding="utf-8") as infile:
            return json.load(infile)
    return {}


def normalize_name(value):
    return re.sub(r"[^a-z0-9]", "", value.lower())


def emphasize_author_names(author_string, name_variants):
    highlighted = author_string
    for variant in sorted(name_variants, key=len, reverse=True):
        pattern = re.compile(rf"(?<!\w){re.escape(variant)}(?!\w)")
        highlighted = pattern.sub(f"<strong>{variant}</strong>", highlighted)
    return highlighted


def extract_venue(bib):
    for key in ("journal", "conference", "booktitle", "publisher", "citation"):
        value = bib.get(key)
        if value:
            return value.strip()
    return "Publication venue unavailable"


def extract_year(bib):
    for key in ("pub_year", "year"):
        value = bib.get(key)
        if value:
            return str(value).strip()
    return ""


def publication_url(scholar_id, pub):
    pub_id = pub.get("author_pub_id", "")
    return pub.get("pub_url") or pub.get("eprint_url") or (
        f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={scholar_id}&citation_for_view={scholar_id}:{pub_id}"
    )


def is_first_authored(author_string, name_variants):
    first_author = author_string.split(",")[0].strip() if author_string else ""
    normalized_first = normalize_name(first_author)
    return normalized_first in {normalize_name(v) for v in name_variants}


def build_publication_data(author, scholar_id, overrides):
    name_variants = overrides.get(
        "name_variants",
        ["J Fu", "Fu J", "Jiye Fu", "FU Jiye"],
    )
    corresponding_ids = set(overrides.get("corresponding_author_ids", []))

    grouped = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "source": "Google Scholar",
        "scholar_id": scholar_id,
        "first_or_corresponding": [],
        "co_authored": [],
    }

    for pub in author.get("publications", {}).values():
        bib = pub.get("bib", {})
        authors = bib.get("author", "").strip()
        pub_id = pub.get("author_pub_id", "")
        entry = {
            "id": pub_id,
            "title": bib.get("title", "").strip(),
            "authors": authors,
            "authors_html": emphasize_author_names(authors, name_variants),
            "venue": extract_venue(bib),
            "year": extract_year(bib),
            "url": publication_url(scholar_id, pub),
            "citation_count": pub.get("num_citations", 0),
        }

        if is_first_authored(authors, name_variants) or pub_id in corresponding_ids:
            grouped["first_or_corresponding"].append(entry)
        else:
            grouped["co_authored"].append(entry)

    sort_key = lambda item: (
        int(item["year"]) if str(item["year"]).isdigit() else 0,
        int(item["citation_count"]),
        item["title"].lower(),
    )
    grouped["first_or_corresponding"].sort(key=sort_key, reverse=True)
    grouped["co_authored"].sort(key=sort_key, reverse=True)
    return grouped


author: dict = scholarly.search_author_id(os.environ["GOOGLE_SCHOLAR_ID"])
scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])
author["updated"] = datetime.now(timezone.utc).isoformat()
author["publications"] = {v["author_pub_id"]: v for v in author["publications"]}

print(json.dumps(author, indent=2))
os.makedirs("results", exist_ok=True)
with open("results/gs_data.json", "w", encoding="utf-8") as outfile:
    json.dump(author, outfile, ensure_ascii=False)

publication_data = build_publication_data(
    author,
    os.environ["GOOGLE_SCHOLAR_ID"],
    load_overrides(),
)
with open("results/google_scholar_publications.json", "w", encoding="utf-8") as outfile:
    json.dump(publication_data, outfile, ensure_ascii=False, indent=2)

shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": f"{author['citedby']}",
}
with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)
