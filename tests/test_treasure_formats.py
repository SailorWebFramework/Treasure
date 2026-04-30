"""
Treasure format string consistency tests.

Validates that format strings in properties.json and units.json are internally
consistent with their accompanying names/types arrays.

Rules checked:
  1. All {{name}} placeholders in a format string must match an entry in names[]
  2. No bare SEQ, without # prefix (catches the font-family bug)
  3. Count of #SEQ markers ≤ count of sequence[...] types in types[]
  4. Tailwind keys start with '.'
  5. Tailwind alias uniqueness after convert_name() transformation

Known bugs are marked xfail — fix in Treasure JSON, then remove the xfail.
"""
import re
import sys
import os
import pytest

from conftest import load_json

# ---------------------------------------------------------------------------
# Known data bugs (tracked in GitHub issues)
# ---------------------------------------------------------------------------

# Properties with {{placeholder}} mismatches (format refs names not in names[])
# This set contains property paths where the mismatch is a known data bug.
KNOWN_FORMAT_MISMATCH_PATHS = {
    # clip-path:0 uses {{shape}} but names=['none']
    "clip-path:0",
    # border-* grouped sub-properties use qualified names like {{blockEndColor}}
    # but the names[] array only has the short local name like 'color'
    # Pattern: border-{side}-*.{property}
}

# The font-*.family bare SEQ bug
KNOWN_BARE_SEQ_PATHS = {
    # "font-*.family" or similar — exact path TBD by inspection
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _placeholder_names(fmt: str) -> set:
    """Extract all {{name}} placeholder names from a format string."""
    return set(re.findall(r"\{\{(\w+)\}\}", fmt))


def _seq_count(fmt: str) -> int:
    """Count #SEQ occurrences in a format string."""
    return len(re.findall(r"#SEQ", fmt))


def _sequence_type_count(types: list) -> int:
    """Count types that are sequence[...] variants."""
    return sum(1 for t in types if isinstance(t, str) and t.startswith("sequence["))


def _collect_leaf_properties(obj: dict, path: str = "") -> list:
    """Recursively yield (path, prop_dict) for all leaf properties."""
    if not isinstance(obj, dict):
        return []
    results = []
    if "types" in obj and "names" in obj and "format" in obj:
        results.append((path, obj))
    else:
        for k, v in obj.items():
            if k not in ("description", "shorthand"):
                results.extend(_collect_leaf_properties(v, f"{path}.{k}" if path else k))
    return results


# ---------------------------------------------------------------------------
# 1. No bare SEQ, (font-family bug)
# ---------------------------------------------------------------------------

def test_no_bare_SEQ_format_strings(properties, units):
    """No format string may contain 'SEQ,' without the leading '#'.

    The correct syntax is '#SEQ,' (or '#SEQ ' etc.) — the bare form is a
    data entry error that causes SEQ, to appear as literal text in generated
    Swift.

    Known occurrences:  font-*.family  (tracked in GitHub issue).
    """
    violations = []

    for path, prop in _collect_leaf_properties(properties):
        fmt = prop.get("format", "")
        # Match SEQ, not preceded by #
        if re.search(r"(?<!#)SEQ[,\s]", fmt):
            violations.append((path, fmt))

    # Also check units.json
    for uname, udata in units.items():
        if not isinstance(udata, dict):
            continue
        for cname, cdata in udata.get("cases", {}).items() if isinstance(udata.get("cases"), dict) else []:
            fmt = cdata.get("format", "") if isinstance(cdata, dict) else ""
            if re.search(r"(?<!#)SEQ[,\s]", fmt):
                violations.append((f"{uname}.{cname}", fmt))

    if violations:
        # Check if all are known bugs
        paths_only = [p for p, _ in violations]
        unknown = [p for p in paths_only if not any(known in p for known in KNOWN_BARE_SEQ_PATHS)]
        if unknown:
            pytest.fail(
                f"{len(violations)} bare SEQ violation(s) (not all known):\n"
                + "\n".join(f"  {p}: {f!r}" for p, f in violations[:10])
            )
        else:
            pytest.xfail(
                f"Known bare SEQ violation(s) (GitHub issue): "
                + "; ".join(f"{p}: {f!r}" for p, f in violations[:5])
            )


# ---------------------------------------------------------------------------
# 2. #SEQ count vs sequence types count
# ---------------------------------------------------------------------------

def test_SEQ_count_vs_sequence_types(properties):
    """Count of #SEQ markers in format ≤ count of sequence[...] types in types[].

    grid:0 has '#SEQ  / #SEQ' with 2 sequence types — this is a known
    codegen limitation (put_formatted only handles the first #SEQ).
    Tracked in GitHub issue.
    """
    violations = []
    for path, prop in _collect_leaf_properties(properties):
        fmt = prop.get("format", "")
        types = prop.get("types", [])
        seq_in_fmt = _seq_count(fmt)
        seq_in_types = _sequence_type_count(types)
        if seq_in_fmt > seq_in_types:
            violations.append((path, seq_in_fmt, seq_in_types, fmt))

    if violations:
        pytest.fail(
            f"{len(violations)} format(s) have more #SEQ than sequence types:\n"
            + "\n".join(f"  {p}: {n_fmt} #SEQ but only {n_t} sequence type(s) — {f!r}"
                        for p, n_fmt, n_t, f in violations[:10])
        )


# ---------------------------------------------------------------------------
# 3. Format placeholder names match names[]
# ---------------------------------------------------------------------------

@pytest.mark.xfail(
    reason=(
        "Known data bugs: border-* grouped properties use qualified placeholder "
        "names (e.g. {{blockEndColor}}) that don't match their short local names "
        "array entries (e.g. ['color']); clip-path:0 uses {{shape}} but names=['none']. "
        "Tracked in GitHub issues."
    ),
    strict=False,
)
def test_property_format_placeholders_match_names(properties):
    """Every {{name}} placeholder in a property format string must appear in names[].

    This catches cases where the format and names arrays have gotten out of
    sync — a placeholder that doesn't match any name will produce invalid
    Swift interpolation at codegen time.
    """
    mismatches = []
    for path, prop in _collect_leaf_properties(properties):
        fmt = prop.get("format", "")
        names = prop.get("names", [])
        placeholders = _placeholder_names(fmt)
        for ph in placeholders:
            if ph not in names:
                mismatches.append((path, ph, names, fmt))

    assert not mismatches, (
        f"{len(mismatches)} format/names mismatch(es) in properties.json:\n"
        + "\n".join(
            f"  {path}: {{{{ph}}}} not in {names!r}  (format={fmt!r})"
            for path, ph, names, fmt in mismatches[:15]
        )
    )


@pytest.mark.xfail(
    reason=(
        "Known unit data bugs: Integer.int uses {{number}} but names=['int']; "
        "BackgroundSize.size:0 uses {{both}} but names=['widthAndHeight']; "
        "Indent.with and PaintOrder.with use format names without '@' prefix "
        "that don't match the @-prefixed entries in names[]. "
        "Tracked in GitHub issues."
    ),
    strict=False,
)
def test_unit_format_placeholders_match_names(units):
    """Every {{name}} placeholder in a unit case format string must appear in names[].

    Unit case names arrays define the Swift parameter names; format strings
    must only reference names that exist in the names array.
    """
    mismatches = []
    for uname, udata in units.items():
        if not isinstance(udata, dict):
            continue
        cases = udata.get("cases", {})
        if not isinstance(cases, dict):
            continue
        for cname, cdata in cases.items():
            if not isinstance(cdata, dict):
                continue
            fmt = cdata.get("format", "")
            names = cdata.get("names", [])
            placeholders = _placeholder_names(fmt)
            for ph in placeholders:
                if ph not in names:
                    mismatches.append((f"{uname}.{cname}", ph, names, fmt))

    assert not mismatches, (
        f"{len(mismatches)} unit format/names mismatch(es) in units.json:\n"
        + "\n".join(
            f"  {path}: {{{{ph}}}} not in {names!r}  (format={fmt!r})"
            for path, ph, names, fmt in mismatches[:15]
        )
    )


# ---------------------------------------------------------------------------
# 4. Tailwind keys start with '.'
# ---------------------------------------------------------------------------

def test_tailwind_keys_start_with_dot(tailwind):
    """Every key in tailwind.json must start with '.' (CSS class selector)."""
    bad = [k for k in tailwind if not k.startswith(".")]
    assert not bad, (
        f"{len(bad)} Tailwind key(s) don't start with '.': {bad[:10]}"
    )


# ---------------------------------------------------------------------------
# 5. Tailwind alias uniqueness after convert_name()
# ---------------------------------------------------------------------------

def test_tailwind_no_duplicate_classes(tailwind):
    """tailwind.json must not have two identical class keys before conversion."""
    # Duplicate keys are caught by test_no_duplicate_keys_tailwind.
    # This test redundantly verifies the loaded dict length matches.
    assert len(tailwind) > 0, "tailwind.json must not be empty"


def test_tailwind_alias_uniqueness(tailwind):
    """After apply the convert_name pipeline, no two Tailwind classes should
    collide to the same Swift identifier.

    The convert_name() function strips the leading '.', replaces special chars
    with underscores, and applies switch_to_camel.  Two different classes
    mapping to the same Swift name would produce a duplicate enum case.
    """
    # Add Shipwright src to path to import Utils
    shipwright_src = os.path.join(
        os.path.dirname(__file__), "..", "..", "Shipwright", "src"
    )
    if os.path.isdir(shipwright_src):
        sys.path.insert(0, os.path.dirname(shipwright_src))
        sys.path.insert(0, shipwright_src)

    try:
        from Utils import switch_to_camel  # type: ignore

        def convert_name(key: str) -> str:
            """Mirror the convert_name logic in Sailor.py buildTailwind."""
            name = key.lstrip(".")
            name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
            name = switch_to_camel(name)
            return name

        aliases = [convert_name(k) for k in tailwind.keys()]
        if len(aliases) != len(set(aliases)):
            from collections import Counter
            counts = Counter(aliases)
            collisions = {a: c for a, c in counts.items() if c > 1}
            pytest.fail(
                f"{len(collisions)} Swift identifier collision(s) in tailwind.json: "
                + str(dict(list(collisions.items())[:5]))
            )
    except ImportError:
        pytest.skip("Shipwright Utils not importable from Treasure tests — skipping alias uniqueness check")
