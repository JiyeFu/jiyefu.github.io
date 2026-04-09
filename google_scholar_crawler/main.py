from scholarly import scholarly
import json
from datetime import datetime, timezone
from pathlib import Path
import os
import re
import difflib
import urllib.parse
import urllib.request


REPO_ROOT = Path(__file__).resolve().parents[1]
OVERRIDES_PATH = REPO_ROOT / "_data" / "scholar_publication_overrides.json"
FEATURE_METADATA_PATH = REPO_ROOT / "_data" / "publication_feature_metadata.json"
CROSSREF_CACHE = {}


def load_overrides():
    if OVERRIDES_PATH.exists():
        with OVERRIDES_PATH.open("r", encoding="utf-8") as infile:
            return json.load(infile)
    return {}


def load_feature_metadata():
    if FEATURE_METADATA_PATH.exists():
        with FEATURE_METADATA_PATH.open("r", encoding="utf-8") as infile:
            return json.load(infile)
    return {"featured_count": 3, "publications": {}}


def normalize_name(value):
    return re.sub(r"[^a-z0-9]", "", value.lower())


def normalize_title(value):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


def emphasize_author_names(author_string, name_variants):
    normalized_variants = {normalize_name(variant) for variant in name_variants}
    highlighted_parts = []
    for part in author_string.split(","):
        author_name = part.strip()
        if normalize_name(author_name) in normalized_variants:
            highlighted_parts.append(f"<strong>{author_name}</strong>")
        else:
            highlighted_parts.append(author_name)
    return ", ".join(highlighted_parts)


def apply_author_role_markers(author_string, author_role_metadata=None):
    author_role_metadata = author_role_metadata or {}
    co_first = {normalize_name(name) for name in author_role_metadata.get("co_first_authors", [])}
    corresponding = {normalize_name(name) for name in author_role_metadata.get("corresponding_authors", [])}

    marked_parts = []
    for part in author_string.split(","):
        author_name = part.strip()
        normalized_author = normalize_name(author_name)
        suffix = ""
        if normalized_author in co_first:
            suffix += "†"
        if normalized_author in corresponding:
            suffix += "*"
        marked_parts.append(f"{author_name}{suffix}")
    return ", ".join(marked_parts)


def extract_venue(bib):
    for key in ("journal", "conference", "booktitle", "publisher", "citation"):
        value = bib.get(key)
        if value:
            return value.strip()
    return "Publication venue unavailable"


def title_case_family_name(value):
    return "-".join(segment.capitalize() for segment in value.split("-") if segment)


def initials_from_given_name(value):
    parts = re.split(r"[\s\-]+", value.strip())
    return "".join(part[0].upper() for part in parts if part)


def format_crossref_author_name(author):
    family = title_case_family_name(author.get("family", "").strip())
    given = author.get("given", "").strip()
    initials = initials_from_given_name(given)
    if initials and family:
        return f"{initials} {family}"
    return family or given


def format_authors(authors, crossref_item=None):
    if crossref_item and crossref_item.get("author"):
        formatted = [
            format_crossref_author_name(author)
            for author in crossref_item.get("author", [])
            if format_crossref_author_name(author)
        ]
        if formatted:
            return ", ".join(formatted)
    return authors


def build_venue_parts(bib, crossref_item=None):
    if not crossref_item:
        venue = extract_venue(bib)
        if "," in venue:
            journal_title, venue_details = venue.split(",", 1)
            return journal_title.strip(), venue_details.strip()
        return venue, ""

    container_titles = crossref_item.get("container-title", [])
    journal_title = container_titles[0].strip() if container_titles else extract_venue(bib)
    volume = str(crossref_item.get("volume", "")).strip()
    issue = str(crossref_item.get("issue", "")).strip()
    page = str(crossref_item.get("page", "")).strip() or str(crossref_item.get("article-number", "")).strip()

    venue_details = ""
    if volume:
        venue_details += volume
    if issue:
        venue_details += f" ({issue})" if venue_details else f"({issue})"
    if page:
        venue_details += f", {page}" if venue_details else page
    return journal_title, venue_details


def format_venue(bib, crossref_item=None):
    journal_title, venue_details = build_venue_parts(bib, crossref_item)
    if venue_details:
        return f"{journal_title} {venue_details}".strip()
    return journal_title.strip()


def extract_year(bib):
    for key in ("pub_year", "year"):
        value = bib.get(key)
        if value:
            return str(value).strip()
    return ""


def scholar_publication_url(scholar_id, pub):
    pub_id = pub.get("author_pub_id", "")
    return pub.get("pub_url") or pub.get("eprint_url") or (
        f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={scholar_id}&citation_for_view={scholar_id}:{pub_id}"
    )


def crossref_lookup(title, year="", rows=5):
    cache_key = (title, str(year), rows)
    if cache_key in CROSSREF_CACHE:
        return CROSSREF_CACHE[cache_key]

    params = urllib.parse.urlencode(
        {
            "query.title": title,
            "rows": rows,
            "select": "DOI,title,published-print,published-online,issued,URL",
        }
    )
    request = urllib.request.Request(
        f"https://api.crossref.org/works?{params}",
        headers={
            "User-Agent": "Codex academic homepage updater (mailto:fujisann006@gmail.com)",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)
    items = payload.get("message", {}).get("items", [])
    CROSSREF_CACHE[cache_key] = items
    return items


def crossref_item_year(item):
    for key in ("published-print", "published-online", "issued"):
        parts = item.get(key, {}).get("date-parts", [])
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def resolve_publication_link(title, scholar_url, year="", link_overrides=None):
    link_overrides = link_overrides or {}
    if title in link_overrides:
        return link_overrides[title], "", None

    normalized_title = normalize_title(title)

    try:
        best_item = None
        best_score = 0.0
        for item in crossref_lookup(title, year=year):
            candidate_title = ""
            titles = item.get("title", [])
            if titles:
                candidate_title = titles[0]
            normalized_candidate = normalize_title(candidate_title)
            score = difflib.SequenceMatcher(None, normalized_title, normalized_candidate).ratio()
            if normalized_candidate == normalized_title:
                score += 0.2
            item_year = crossref_item_year(item)
            if year and item_year and item_year == str(year):
                score += 0.05
            if score > best_score:
                best_item = item
                best_score = score

        if best_item and best_score >= 0.92:
            doi = best_item.get("DOI", "")
            if doi:
                return f"https://doi.org/{doi}", doi, best_item
            if best_item.get("URL"):
                return best_item["URL"], "", best_item
    except Exception:
        pass

    return scholar_url, "", None


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
    link_overrides = overrides.get("link_overrides", {})
    author_role_overrides = overrides.get("author_role_overrides", {})

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
        scholar_url = scholar_publication_url(scholar_id, pub)
        resolved_url, doi, crossref_item = resolve_publication_link(
            bib.get("title", "").strip(),
            scholar_url,
            year=extract_year(bib),
            link_overrides=link_overrides,
        )
        journal_title, venue_details = build_venue_parts(bib, crossref_item)
        formatted_authors = format_authors(authors, crossref_item)
        marked_authors = apply_author_role_markers(
            formatted_authors,
            author_role_overrides.get(pub_id, {}),
        )
        entry = {
            "id": pub_id,
            "title": bib.get("title", "").strip(),
            "authors": marked_authors,
            "authors_html": emphasize_author_names(marked_authors, name_variants),
            "journal_title": journal_title,
            "venue_details": venue_details,
            "venue": format_venue(bib, crossref_item),
            "year": extract_year(bib),
            "url": resolved_url,
            "doi": doi,
            "scholar_url": scholar_url,
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


def add_featured_publications(grouped, feature_metadata):
    allowed_types = {"research", "database", "letter"}
    publication_meta = feature_metadata.get("publications", {})
    featured_count = int(feature_metadata.get("featured_count", 3))

    all_publications = grouped["first_or_corresponding"] + grouped["co_authored"]
    featured_candidates = []

    for entry in all_publications:
        meta = publication_meta.get(entry["id"], {})
        article_type = meta.get("article_type", "").lower()
        journal_rank = meta.get("journal_rank")
        if article_type not in allowed_types or journal_rank is None:
            continue

        candidate = dict(entry)
        candidate["article_type"] = article_type
        candidate["journal_rank"] = journal_rank
        candidate["tags"] = meta.get("tags", [])
        featured_candidates.append(candidate)

    featured_candidates.sort(
        key=lambda item: (
            int(item["journal_rank"]),
            -int(item["year"]) if str(item["year"]).isdigit() else 0,
            -int(item["citation_count"]),
            item["title"].lower(),
        )
    )
    grouped["featured_publications"] = featured_candidates[:featured_count]
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
publication_data = add_featured_publications(
    publication_data,
    load_feature_metadata(),
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
