# Writing Criteria

Every guide in this repo is written to the same
standard. If you're adding or editing a guide —
human or AI — hold it to these.

1. **Plain words, real ideas.** Simple language,
   never dumbed-down concepts. Explain jargon on
   first use; collect terms in the glossary.
2. **No hype.** No marketing adjectives, no
   "revolutionary," no promises about what
   something will do for the reader.
3. **Honest about limits.** Say what the thing
   *can't* do. State uncertainty instead of
   smoothing it over. Validation notes include
   what remains unverified.
4. **No invented numbers.** Benchmarks, defaults,
   and specs are either measured or qualified with
   "depends on your setup." If it wasn't tested,
   say so.
5. **Checkable.** Commands are meant to be run,
   with "Check:" blocks showing what success looks
   like. Sources are linked, not asserted.
6. **Respect the reader's setup.** Call out
   Windows/Mac/Linux differences. Don't assume a
   GPU, a budget, or prior experience.
7. **Safety isn't skipped.** Real risks get
   stated plainly, not buried.
8. **Scoped.** Each guide says what it covers and
   points elsewhere for the rest. No guide
   pretends to be the whole subject.
9. **Structure over prose.** Tables, before/after
   examples, symptom → fix. Scannable beats essay.

## Verification notes for this guide

Standard 3 and 4 applied to this guide,
specifically. YAML's entire everyday surface is
parsers in a terminal, so — like its predecessor
in this series — essentially all of it ran.

**The tools, and how they were obtained:**
PyYAML **6.0.3** and yamllint **1.38.0**,
pip-installed in a scratch virtualenv used for
the build; **yq 4.47.2** (mikefarah, a YAML 1.2
parser), a single binary downloaded from the
project's releases for the cross-parser chapter;
**jq 1.7**, already installed, for two commands
in the worked example. The reference parser is
PyYAML throughout, and the chapters say so:
PyYAML follows the **YAML 1.1** rules, which is
precisely why it can demonstrate the 1.1 traps
for real instead of describing them.

**The data:** every file in `examples/` is
invented for this guide — one fictional service
config (`service.yml`), small files per feature
(`types.yml`, `blocks.yml`, `anchors.yml`,
`documents.yml`, `traps.yml`), one JSON file
(`data.json`), and four files broken on purpose
for the error chapters (`broken-colon.yml`,
`broken-tabs.yml` — its indentation is a real
tab character — `broken-indent.yml`,
`broken-stray.yml`), each labelled as broken in
its own header. Commands were run from inside
`examples/` so file names appear exactly as a
reader would type them. `show.py` and
`validate.py` ship in `examples/` and were used
as shipped.

**Verified by running (every quoted output is a
capture, transcribed into the chapter):**

- JSON parsed as YAML: `data.json` loads under
  `safe_load`, prints back as the same JSON, and
  compares equal (`True`) to Python's JSON
  parser's result.
- Structure: `service.yml`'s six top-level keys
  in file order, the nested `server.tls` mapping,
  the checks targets printed from the list of
  maps, and the comment rule — `#` after a space
  starts a comment, glued to a word it stays in
  the value (`beacon#old`).
- Scalars (`types.yml` via `show.py`, every row
  shown): three string styles including the
  doubled-quote escape and the `\t` escape made
  visible by `repr`; `1_000` → 1000; `060` → 48
  (leading-zero octal); `1.2e+3` → 1200.0 while
  `1.2e3` stays a string; `true`/`yes`/`on`/`off`
  all boolean under 1.1; `null`, `~`, and empty
  all None; `''` a string. Also probed and
  stated in the text: `.5` → 0.5, `0x1F` → 31,
  `0o17` a string, `.inf`/`.nan` floats.
- Flow style: `[8080, 8443]`, a flow mapping,
  and a flow list of lists all parse to the same
  structures as their block forms.
- Block scalars: literal, literal-strip, folded,
  folded-strip, and keep (`|+`) on the same
  text, each printed with `repr` so every
  newline is accounted for, plus a shell script
  held whole in a literal block.
- Anchors and merges: the three environments of
  `anchors.yml` resolved (via `show.py`), the
  `production` mapping printed as JSON, alias
  identity (`alerts_to is oncall` → `True`), and
  a two-anchor merge pinning down precedence —
  earlier alias wins, explicit key wins overall.
  yq also resolves the merges (its
  `.production` output is the merged mapping);
  verified, though only PyYAML output is quoted.
- Documents: `safe_load_all` yields the three
  documents of `documents.yml` in order;
  `safe_load` on the same file raises
  ComposerError ("expected a single document in
  the stream … but found another document"),
  quoted verbatim. The release date parses to a
  Python `date` object, the timestamp to a
  `datetime`. Content placed after a `...`
  end marker without a following `---` is an
  error in PyYAML ("expected '<document
  start>'"), and with the `---` it loads as a
  second document — both run; the chapter states
  the rule from the error.
- Tags: `!!str 8080` → `'8080'`, `!!int "8080"`
  → `8080`, and an unknown tag refused by the
  safe loader with ConstructorError, quoted
  verbatim including its caret pointer.
- The traps, all of them, on `traps.yml`:
  `country: NO` → `False`, the whole
  yes/no/on/off family boolean, `1:20` → 80 and
  `12:30:15` → 45015 (sexagesimal), `1.20` → 1.2
  and `2.0` → float, date and timestamp objects,
  and the key `on` returned as the key `True`.
- The cross-parser contrast, same file through
  yq 4.47.2 as JSON: all boolean/date/clock
  traps come back as strings and the key is
  `"on"` again — but `version` is still `1.2`
  and `release` the number `2`. The 1.2
  rulebook fixes the words, not the numbers;
  both tables are quoted whole so readers can
  compare line by line.
- Duplicate keys: `duplicate-keys.yml` loads
  silently keeping the last value (`retries` 5);
  yamllint — its `key-duplicates` rule is on in
  the default ruleset and in the shipped
  `.yamllint` — reports it as an error, exit 1,
  quoted verbatim.
- The worked example: `service.yml` converted
  to JSON with yq (first 20 lines quoted), two
  jq queries over it, `validate.py` reporting
  VALID with exit 0, and — on a scratch copy
  with `port: eighty` — INVALID with exit 1,
  the FAIL line naming the value.
- Dumping: `safe_dump`'s sorted keys, its
  protective quoting of the strings `'yes'` and
  `'2026-10-17'`, its 80-column wrap of a long
  string, `null` spelled out, the flush-left
  sequence style on the dumped `service.yml`,
  round-trip equality (`True`) with reordered
  keys, and `sort_keys=False` preserving order.
- yamllint under the shipped `.yamllint`: the
  duplicate-key error above; `truthy` warnings
  on `service.yml` (line 44, the `off`) and on
  six lines of `traps.yml`, with exit 0 —
  warnings advise, errors fail; and its
  one-line syntax reports for the broken files.
- Safe loading, the full trio on one payload:
  bare `yaml.load(...)` raises TypeError in
  PyYAML 6 (Loader is a required argument);
  `unsafe_load` on an `os.system` payload
  *executed* the embedded `echo` — its output
  and the returned `{'x': 0}` are quoted as
  captured; `safe_load` on the same payload
  raises ConstructorError, quoted verbatim.
- The error gallery, one shipped broken file
  per message, each quoted from the traceback's
  tail: "mapping values are not allowed here"
  (colon, line 5 col 17), "found character '\t'
  that cannot start any token" (tab, line 6),
  "expected <block end>, but found '<block
  mapping start>'" (indent, with both of the
  parser's positions), and "could not find
  expected ':'" (stray line — reported at the
  line *after* the fault, which the chapter
  explains). The colon fix is shown working;
  the indent fix is applied with `sed` and the
  result converted to JSON as the method
  chapter prescribes.

**Stated but not run (documented knowledge):**

- Installation on the reader's machine
  (`pip install pyyaml` / `yamllint`, obtaining
  yq) is described, not performed as part of the
  guide's commands — the build machine installed
  them its own way, and criteria 6 applies.
- The `x-` prefix convention for parking
  anchored defaults where a program ignores
  them, and the note that merge resolution is
  the consumer's behaviour to check, are
  presented as conventions to verify against
  the reader's own tool — parser support varies
  and no single run could settle them.
- Behaviour of parsers other than PyYAML and
  yq (Ruby's psych, Go's gopkg.in/yaml, Rust's
  serde_yaml) is not claimed anywhere in the
  guide; where 1.1-vs-1.2 behaviour matters, the
  two parsers that were run carry the point.

A note on versions: error-message wording,
exit behaviour, and implicit-typing details are
PyYAML 6.0.3's as captured; the yamllint
findings are 1.38.0's under the shipped
`.yamllint`. Other versions mostly agree, and
where the guide knows they don't — YAML 1.1
versus 1.2 — the text says so.
