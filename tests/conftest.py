"""Shared fixtures for Treasure JSON tests."""
import json
import os
import pytest

TREASURE_DIR = os.path.join(os.path.dirname(__file__), "..", "json")
SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), "schemas")


def load_json(filename: str) -> dict:
    """Load a JSON file from the Treasure json/ directory."""
    path = os.path.join(TREASURE_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_json_with_duplicate_check(filename: str) -> dict:
    """Load JSON, raising ValueError on duplicate keys."""
    path = os.path.join(TREASURE_DIR, filename)
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    seen_keys = []

    def raise_on_duplicate(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError(f"Duplicate key {k!r} in {filename}")
            d[k] = v
        return d

    return json.loads(raw, object_pairs_hook=raise_on_duplicate)


def load_schema(name: str) -> dict:
    """Load a JSON Schema from tests/schemas/."""
    path = os.path.join(SCHEMAS_DIR, name)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def units():
    return load_json("units.json")


@pytest.fixture
def properties():
    return load_json("properties.json")


@pytest.fixture
def tags():
    return load_json("tags.json")


@pytest.fixture
def tailwind():
    return load_json("tailwind.json")


@pytest.fixture
def events():
    return load_json("events.json")


@pytest.fixture
def methods():
    return load_json("methods.json")


@pytest.fixture
def global_attributes():
    return load_json("global-attributes.json")
