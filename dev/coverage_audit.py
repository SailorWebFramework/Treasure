#!/usr/bin/env python3
"""Coverage audit: diff Treasure JSON against canonical HTML/CSS/event lists.

Fetches WHATWG element and event lists via w3c/webref and the CSS property list
from mdn/data, then reports what Treasure is missing. Run from the repo root:

    python3 dev/coverage_audit.py
"""
import json, os, sys, urllib.request

JSON = os.path.join(os.path.dirname(__file__), "..", "json")
SOURCES = {
    "elements": "https://raw.githubusercontent.com/w3c/webref/main/ed/elements/html.json",
    "html_events": "https://raw.githubusercontent.com/w3c/webref/main/ed/events/html.json",
    "ui_events": "https://raw.githubusercontent.com/w3c/webref/main/ed/events/uievents.json",
    "css": "https://raw.githubusercontent.com/mdn/data/main/css/properties.json",
}

# SVG presentation properties are out of scope for Treasure.
SVG_ONLY = {
    "alignment-baseline", "baseline-shift", "cx", "cy", "d", "dominant-baseline", "fill",
    "flood-color", "flood-opacity", "lighting-color", "marker", "marker-end", "marker-mid",
    "marker-start", "path-length", "r", "rx", "ry", "stop-color", "stop-opacity", "stroke",
    "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin",
    "stroke-miterlimit", "stroke-opacity", "stroke-width", "text-anchor", "vector-effect",
    "x", "y", "color-interpolation-filters",
}
# Events that only fire on window/document/workers, never on an element.
NON_ELEMENT_EVENTS = {
    "DOMActivate", "DOMContentLoaded", "DOMFocusIn", "DOMFocusOut", "afterprint", "beforeprint",
    "beforeunload", "connect", "currententrychange", "dispose", "hashchange", "languagechange",
    "message", "messageerror", "navigate", "navigateerror", "navigatesuccess", "offline",
    "online", "open", "pagehide", "pagereveal", "pageshow", "pageswap", "popstate",
    "readystatechange", "rejectionhandled", "storage", "unhandledrejection", "unload",
    "visibilitychange", "textInput", "enter", "exit", "addtrack", "removetrack",
}
GLOBAL_ATTRIBUTES = {
    "accesskey", "anchor", "autocapitalize", "autocorrect", "autofocus", "class",
    "contenteditable", "dir", "draggable", "enterkeyhint", "exportparts", "hidden", "id",
    "inert", "inputmode", "is", "itemid", "itemprop", "itemref", "itemscope", "itemtype",
    "lang", "nonce", "part", "popover", "role", "slot", "spellcheck", "style", "tabindex",
    "title", "translate", "virtualkeyboardpolicy", "writingsuggestions",
}


def fetch(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def load(name):
    with open(os.path.join(JSON, name)) as f:
        return json.load(f)


def treasure_css_names(props):
    """Expand grouped keys: 'border-*' -> border-<sub>, 'animation:0' -> animation."""
    names = set()
    for key, value in props.items():
        if key.endswith("-*"):
            for sub in value:
                names.add(f"{key[:-2]}-{sub}".split(":")[0])
        else:
            names.add(key.split(":")[0])
    return names


def section(title, have, want, label_have="Treasure", label_want="spec"):
    covered = have & want
    print(f"\n== {title}: {len(covered)}/{len(want)} ({len(covered) / len(want):.0%}) ==")
    missing = sorted(want - have)
    if missing:
        print(f"missing ({len(missing)}): " + ", ".join(missing))
    extra = sorted(have - want)
    if extra:
        print(f"{label_have}-only ({len(extra)}): " + ", ".join(extra))
    return missing


def main():
    tags, props, events, ga = load("tags.json"), load("properties.json"), load("events.json"), load("global-attributes.json")
    src = {k: fetch(v) for k, v in SOURCES.items()}

    elements = {e["name"] for e in src["elements"]["elements"]}
    section("HTML elements", set(tags), elements)

    std = {k for k, v in src["css"].items() if v.get("status") == "standard" and not k.startswith("-")}
    section("CSS properties (MDN standard, non-SVG)", treasure_css_names(props), std - SVG_ONLY)

    canon_events = {e["type"] for e in src["html_events"]["events"]} | {e["type"] for e in src["ui_events"]["events"]}
    have_events = set(events["global"])
    for group in events["targeted"].values():
        have_events |= set(group["events"])
    section("Element events (HTML + UI Events specs)", have_events, canon_events - NON_ELEMENT_EVENTS)

    section("Global attributes (MDN)", set(ga), GLOBAL_ATTRIBUTES)

    no_attrs = sorted(t for t, v in tags.items() if not v.get("attributes"))
    print(f"\n== tags with no element-specific attributes: {len(no_attrs)}/{len(tags)} ==")
    print(", ".join(no_attrs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
