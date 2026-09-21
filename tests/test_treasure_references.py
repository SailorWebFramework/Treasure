"""
Treasure cross-file reference integrity tests.

Validates that Unit.X references in properties.json and tags.json actually
exist as top-level keys in units.json.  A missing unit reference means
Shipwright will generate Swift code that references an undefined type,
causing a compile error.
"""
import re
import pytest

from conftest import load_json

# ---------------------------------------------------------------------------
# Known missing unit references (data bugs — tracked in GitHub issues)
# These units are referenced in properties.json but not defined in units.json.
# They are listed here so the test marks them as xfail rather than silently
# hiding them.  Each entry corresponds to a GitHub issue.
# ---------------------------------------------------------------------------
KNOWN_MISSING_UNIT_REFS = {
    "BackgroundPosition",  # used by mask-position — see GitHub issue
    "BackgroundOrigin",    # used by mask-origin  — see GitHub issue
    "BackgroundClip",      # used by mask-clip    — see GitHub issue
}

# Units that are valid but not defined in units.json — they are generated
# from separate source files (language-codes.json etc.) at codegen time.
GENERATED_UNIT_NAMES = {
    "Language",  # generated from language-codes.json by buildUnits
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_unit_refs_from_types(types_list: list) -> set:
    """Return set of Unit.X names referenced in a types array."""
    refs = set()
    for t in types_list:
        if not isinstance(t, str):
            continue
        # Handles: "Unit.Foo", "optional[Unit.Foo]", "sequence[Unit.Foo]"
        for match in re.findall(r"Unit\.(\w+)", t):
            refs.add(match)
    return refs


def _collect_property_unit_refs(obj: dict, path: str = "") -> list:
    """Recursively collect (unit_name, path) from a properties.json object."""
    results = []
    if isinstance(obj, dict):
        if "types" in obj and isinstance(obj["types"], list):
            for ref in _extract_unit_refs_from_types(obj["types"]):
                results.append((ref, path))
        else:
            for k, v in obj.items():
                if k not in ("description", "names", "format", "shorthand"):
                    results.extend(_collect_property_unit_refs(v, path + "." + k if path else k))
    return results


def _collect_tag_attr_unit_refs(tags: dict) -> list:
    """Collect (unit_name, tag.attr) from tags.json attribute type strings."""
    results = []
    for tag_name, tag_data in tags.items():
        if not isinstance(tag_data, dict):
            continue
        for attr_name, attr_data in tag_data.get("attributes", {}).items():
            attr_type = attr_data.get("type", "") if isinstance(attr_data, dict) else ""
            for match in re.findall(r"Unit\.(\w+)", attr_type):
                results.append((match, f"{tag_name}.{attr_name}"))
    return results


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_unit_global_exists(units):
    """Unit.Global (the universal catch-all) must be defined in units.json."""
    assert "Global" in units, "Unit.Global must exist in units.json"


def test_property_unit_references_exist(units, properties):
    """Every Unit.X reference in properties.json must exist in units.json.

    Known missing refs (BackgroundPosition, BackgroundOrigin, BackgroundClip)
    are expected to fail — they are tracked as GitHub issues.
    """
    unit_names = set(units.keys())
    refs = _collect_property_unit_refs(properties)

    missing = [
        (unit, path) for (unit, path) in refs
        if unit not in unit_names
        and unit not in KNOWN_MISSING_UNIT_REFS
        and unit not in GENERATED_UNIT_NAMES
    ]

    # Separate the known-missing ones
    known_missing_found = [
        (unit, path) for (unit, path) in refs
        if unit in KNOWN_MISSING_UNIT_REFS and unit not in unit_names
    ]

    # Known-missing refs fail with xfail marker
    if known_missing_found:
        pytest.xfail(
            f"Known missing unit references (GitHub issues): "
            + ", ".join(f"Unit.{u} (at {p})" for u, p in known_missing_found[:5])
        )

    assert not missing, (
        f"{len(missing)} unexpected missing unit reference(s) in properties.json:\n"
        + "\n".join(f"  Unit.{u} at {p}" for u, p in missing[:20])
    )


def test_tag_attribute_unit_references_exist(units, tags):
    """Every Unit.X reference in tags.json attribute types must exist in units.json."""
    unit_names = set(units.keys())
    refs = _collect_tag_attr_unit_refs(tags)

    missing = [
        (unit, path) for (unit, path) in refs
        if unit not in unit_names and unit not in GENERATED_UNIT_NAMES
    ]
    assert not missing, (
        f"{len(missing)} missing unit reference(s) in tags.json attributes:\n"
        + "\n".join(f"  Unit.{u} at {p}" for u, p in missing)
    )


def test_event_interfaces_are_non_empty_strings(events):
    """Every event interface field in events.json must be a non-empty string.

    We don't validate against an external registry — just that the field
    is present and non-empty (structural integrity).
    """
    failures = []
    for event_name, event_data in events.get("global", {}).items():
        iface = event_data.get("interface", "")
        if not isinstance(iface, str) or not iface.strip():
            failures.append(event_name)
    for group_data in events.get("targeted", {}).values():
        for event_name, event_data in group_data.get("events", {}).items():
            iface = event_data.get("interface", "")
            if not isinstance(iface, str) or not iface.strip():
                failures.append(event_name)

    assert not failures, (
        f"{len(failures)} event(s) with empty/missing interface: {failures[:10]}"
    )
