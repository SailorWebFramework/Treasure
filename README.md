# Treasure

The HTML/CSS specification that Sailor is generated from. Everything in `json/` is data;
[Shipwright](https://github.com/SailorWebFramework/Shipwright) turns it into strongly typed
Swift for [Sailor](https://github.com/SailorWebFramework/Sailor).

| File | Contents |
|---|---|
| `tags.json` | HTML elements, their descriptions, attributes and whether they are void. |
| `global-attributes.json` | Attributes shared by every element. |
| `events.json` | DOM events, grouped by the elements that fire them, with the payload each one exposes. |
| `methods.json` | Imperative DOM methods exposed on typed element handles. |
| `properties.json` | CSS properties and the unit types each accepts. |
| `units.json` | CSS unit/value types (lengths, colors, keywords, …). |
| `tailwind.json` | Tailwind v3 utility classes for Fleet-Tailwind. |
| `language-codes.json` | `lang` attribute values. |
| `config.json` | Codegen configuration. |

## Editing

Every property in `properties.json` references unit types by name (`Unit.Length`, `Unit.Color`, …)
that must exist in `units.json`, and every `{{placeholder}}` in a property's format string must
appear in that property's `names[]`. The test suite checks these invariants:

```bash
pip install -r requirements-test.txt
pytest tests/
```

`tests/schemas/` holds a JSON schema per file. After changing JSON, regenerate Sailor with
Shipwright and confirm it still compiles — the Codegen → Compile smoke job in Shipwright's CI
does exactly this for every push.

## Coverage

CSS property coverage is tracked in
[Treasure #1](https://github.com/SailorWebFramework/Treasure/issues/1);
`dev/completed.json` records what has been audited so far.
