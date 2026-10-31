"""Read the public editorial workbook and produce a validated publication."""
import csv
import io
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {
    "Site": ["key", "value"],
    "Pages": ["id", "heading", "body", "publish"],
    "Projects": ["id", "title", "theme", "summary", "url", "invite", "publish"],
    "Sources": ["id", "name", "theme", "scope", "summary", "url", "contact_route", "checked_on", "status", "publish"],
    "Places": ["code", "name", "region", "stage", "resident_contacts", "communities", "notes", "publish"],
}
SETTING_KEYS = {"title", "strapline", "contact_email"}
THEMES = {"law", "resilience", "technology", "cooperation", "culture", "civic", "community", "education", "livelihoods"}
REGIONS = {"Africa", "Americas", "Asia", "Europe", "Oceania"}
STAGES = {"Seeking contacts", "Route identified", "In conversation", "Resident connection"}

def safe_url(value):
    p = urlparse(str(value))
    if p.scheme != "https" or not p.hostname or p.username or p.password or any(c in value for c in "\r\n"):
        raise ValueError("Public links must be HTTPS URLs without credentials")
    return str(value)

def rows_from_csv(text, tab):
    if tab not in FIELDS:
        raise ValueError("This is not an allowed public CMS tab")
    reader = csv.DictReader(io.StringIO(text.lstrip("\ufeff")))
    if reader.fieldnames != FIELDS[tab]:
        raise ValueError(f"{tab}: expected the documented public columns exactly")
    result = []
    for row in reader:
        if None in row:
            raise ValueError(f"{tab}: a row has extra cells")
        if not any(str(v or "").strip() for v in row.values()):
            continue
        row = {k: str(v or "").strip() for k, v in row.items()}
        if "publish" in row:
            if row["publish"] not in {"Yes", "No"}:
                raise ValueError(f"{tab}: publication must be Yes or No")
            if row["publish"] == "No":
                continue
        result.append(row)
    return result

def validate(data):
    if set(data) - {"settings", "projects", "sources", "places", "pages", "meta", "config"}:
        raise ValueError("Publication contains an unexpected top-level record set")
    if set(data["settings"]) - SETTING_KEYS:
        raise ValueError("Unexpected setting in the public CMS")
    email = data["settings"].get("contact_email", "")
    if not re.fullmatch(r"[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+", email):
        raise ValueError("A valid published project contact address is required")
    mapping = {"projects": "Projects", "sources": "Sources", "places": "Places", "pages": "Pages"}
    for collection, tab in mapping.items():
        ids = set()
        for row in data.get(collection, []):
            if set(row) - set(FIELDS[tab]):
                raise ValueError(f"Unexpected fields in {tab}")
            key = row.get("id", row.get("code", ""))
            if not key or key in ids:
                raise ValueError(f"{tab}: empty or duplicate ID")
            ids.add(key)
            if "url" in row and row["url"]:
                safe_url(row["url"])
            if "theme" in row and row["theme"] not in THEMES:
                raise ValueError(f"{tab}: unknown theme")
            if collection == "places":
                if not re.fullmatch("[A-Z]{2}", row["code"]) or row["region"] not in REGIONS:
                    raise ValueError("Invalid reference place")
                if row["stage"] not in STAGES:
                    raise ValueError("Unknown contact stage")
                for field in ["resident_contacts", "communities"]:
                    value = row[field]
                    if not re.fullmatch(r"\d+", str(value)):
                        raise ValueError("Public contact totals must be nonnegative whole numbers")
                    row[field] = int(value)
                if row["stage"] == "Resident connection" and row["resident_contacts"] < 1:
                    raise ValueError("A resident connection needs a confirmed resident count")
    return data

def load_public(offline=False):
    config = json.loads((ROOT / "cms.config.json").read_text())
    sheet_id = (os.environ.get("CMS_SPREADSHEET_ID") or config.get("spreadsheet_id", "")).strip()
    if sheet_id and not offline:
        if not re.fullmatch(r"[A-Za-z0-9_-]{20,}", sheet_id):
            raise ValueError("Invalid CMS spreadsheet ID")
        tables = {}
        for tab in FIELDS:
            query = urlencode({"tqx": "out:csv", "sheet": tab, "headers": "1"})
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?{query}"
            request = Request(url, headers={"User-Agent": "OutreachCMS/1.0 public-content publisher"})
            with urlopen(request, timeout=25) as response:
                payload = response.read(3_000_001)
            if len(payload) > 3_000_000:
                raise ValueError(f"{tab} exceeds the public import size limit")
            tables[tab] = rows_from_csv(payload.decode("utf-8-sig"), tab)
        data = {"settings": {r["key"]: r["value"] for r in tables["Site"]},
                "pages": tables["Pages"], "projects": tables["Projects"],
                "sources": tables["Sources"], "places": tables["Places"]}
        mode = "Google Sheets"
    else:
        data = json.loads((ROOT / "data/seed.json").read_text())
        data.setdefault("pages", [])
        for collection in ["projects", "sources", "places", "pages"]:
            data[collection] = [r for r in data[collection] if r.get("publish", "Yes") == "Yes"]
        mode = "Source snapshot"
    data["config"] = {k: safe_url(v) if v else "" for k, v in config.items() if k.endswith("_url")}
    data["meta"] = {"mode": mode, "built_at": datetime.now(timezone.utc).isoformat(),
                    "source_date": "2026-10-31", "run_url": ""}
    if os.environ.get("GITHUB_RUN_ID"):
        data["meta"]["run_url"] = f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
    return validate(data)

