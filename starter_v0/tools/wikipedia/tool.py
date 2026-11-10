from __future__ import annotations

from typing import Any
from urllib.parse import quote

import requests

from tools._shared import TIMEOUT, err

# Wikimedia asks API clients to identify themselves; a generic name, no personal contact.
HEADERS = {"User-Agent": "ManDanResearchAgent/0.1 (VinUni AI lab)"}
LANGS = ("vi", "en")


def wikipedia_summary(title: str = "", lang: str = "vi") -> dict[str, Any]:
    """Lead-section summary of one Wikipedia page (REST page/summary, no API key)."""
    title = (title or "").strip() if isinstance(title, str) else ""
    if not title:
        return {"tool": "wikipedia", "error": "invalid_input", "message": "title is required"}
    if lang not in LANGS:
        return {"tool": "wikipedia", "error": "invalid_input", "message": f"lang must be one of {LANGS}"}
    try:
        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(title.replace(' ', '_'), safe='')}"
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 404:
            return {"tool": "wikipedia", "error": "not_found", "lang": lang, "title": title,
                    "message": f"No {lang}.wikipedia.org page titled {title!r}; try lang={'en' if lang == 'vi' else 'vi'} or a more exact title."}
        response.raise_for_status()
        data = response.json()
        return {
            "tool": "wikipedia",
            "lang": lang,
            "title": data.get("title"),
            "description": data.get("description"),
            "summary": data.get("extract"),
            "url": ((data.get("content_urls") or {}).get("desktop") or {}).get("page"),
            "ambiguous": data.get("type") == "disambiguation",
        }
    except Exception as exc:
        return err("wikipedia", exc)
