# Glossary

**Alias** — a reference to an anchored value,
written `*name`. Wherever an alias appears, the
anchored value is what the parser delivers.

**Anchor** — a name attached to a value where
it's defined, written `&name`, so the value can
be reused by alias or merged elsewhere.

**Block style** — the indented layout: mappings
as `key: value` lines, sequences as `- ` lines.
The opposite of **flow style**.

**Chomping** — what happens to a block scalar's
final newline: *clip* (keep one, the default),
*strip* (keep none, `-`), or *keep* (keep all
trailing blank lines too, `+`).

**Document** — one complete value in a YAML
stream. Files usually hold one; several are
separated by `---` lines and loaded with an
`_all`-style loader.

**Dump** — turning data structures back into
YAML text (`yaml.safe_dump` in Python). Keys
come out sorted, comments don't survive, and
strings that would re-read as another type are
quoted for protection.

**Explicit tag** — a type written into the
file: `!!str 8080`. Overrides the parser's
implicit guess; rarely needed beyond forcing.

**Flow style** — the bracketed one-line layout,
`[8080, 8443]` and `{name: beacon}`, borrowed
from JSON. Any collection can be written either
way.

**Folded scalar** — a block scalar introduced
by `>`: single line breaks become spaces, for
prose. Its sibling, the **literal scalar** (`|`),
keeps line breaks exactly.

**Implicit typing** — the parser's rules for
guessing a scalar's type from its shape: digits
become numbers, certain words booleans,
date-shaped text (in some parsers) dates.
Chapter 8 is what happens when it guesses
wrong.

**Key** — the left side of a mapping entry.
Keys are values too and get implicit typing of
their own — which is how `on:` becomes the key
`True` under YAML 1.1 rules.

**Mapping** — key/value pairs; what Python calls
a dict and JSON calls an object. Written
`key: value`, one per line.

**Merge key** — `<<`, whose value is an alias
(or list of aliases) to a mapping whose keys
are poured into the current one. Keys written
out locally win.

**Node** — any single piece of a YAML document:
a scalar, a sequence, or a mapping. The word
parsers and the specification use.

**Null** — YAML's "no value", spelled `null`,
`~`, or nothing after the colon. Not the same
as the empty string `''`.

**Plain scalar** — an unquoted value: `beacon`,
`8080`, `1:20`. Cheapest to write, and the only
style the parser freely reinterprets.

**Safe loader** — a loader that constructs only
plain data (strings, numbers, booleans, lists,
mappings, standard types) and refuses tags that
name program objects. The only loader to use
on files you didn't write.

**Scalar** — a single value: string, number,
boolean, or null.

**Sequence** — an ordered list, written with
`- ` lines in block style or `[ ]` in flow.

**Sexagesimal** — base-60 notation, `1:20`
meaning 80 under YAML 1.1 number rules. Removed
in YAML 1.2; one of the famous traps until
then.

**Stream** — a whole YAML input: one or more
documents, possibly with `---` separators and
`...` end markers.

**YAML 1.1 / 1.2** — the two specification
versions in circulation. They agree on structure
and disagree on some scalar spellings — which
words are booleans, whether `1:20` is a number,
whether a timestamp becomes a date object.
"Know your parser" is the short version.
