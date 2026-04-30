"""
Treasure JSON schema validation tests.

Validates each Treasure JSON file against its committed JSON Schema.
Catches structural errors (missing required fields, wrong types) before
Shipwright codegen runs.
"""
import os
import pytest
import jsonschema

from conftest import load_json, load_schema, TREASURE_DIR

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def validate(instance, schema_name: str):
    """Validate *instance* against the named schema; raise on failure."""
    schema = load_schema(schema_name)
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        messages = [f"  [{'.'.join(str(p) for p in e.path)}] {e.message}" for e in errors[:10]]
        raise AssertionError(
            f"{len(errors)} schema violation(s) in {schema_name}:\n" + "\n".join(messages)
        )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_units_schema_valid():
    """units.json must match units.schema.json."""
    data = load_json("units.json")
    validate(data, "units.schema.json")


def test_properties_schema_valid():
    """properties.json must match properties.schema.json.

    Note: properties.json has a complex polymorphic structure (simple /
    group / numbered overload).  The schema uses oneOf to permit both
    leaf SimpleProperty objects and GroupProperty wrappers.
    Properties whose keys are groups (e.g. 'align-*') only contain nested
    sub-property objects without top-level 'types'/'names', and will be
    validated against the GroupProperty variant.
    """
    data = load_json("properties.json")
    validate(data, "properties.schema.json")


def test_tags_schema_valid():
    """tags.json must match tags.schema.json."""
    data = load_json("tags.json")
    validate(data, "tags.schema.json")


def test_tailwind_schema_valid():
    """tailwind.json must match tailwind.schema.json.

    Every key should start with '.' (checked separately in test_treasure_formats).
    The schema validates that values are non-empty strings.
    """
    data = load_json("tailwind.json")
    validate(data, "tailwind.schema.json")


def test_events_schema_valid():
    """events.json must match events.schema.json."""
    data = load_json("events.json")
    validate(data, "events.schema.json")


def test_methods_schema_valid():
    """methods.json must match methods.schema.json."""
    data = load_json("methods.json")
    validate(data, "methods.schema.json")


def test_global_attributes_schema_valid():
    """global-attributes.json must match global-attributes.schema.json."""
    data = load_json("global-attributes.json")
    validate(data, "global-attributes.schema.json")
