# The Famous Traps

Every line of `traps.yml` is valid YAML. It
parses without a warning. And almost none of it
means what it looks like:

```yaml
country: NO
norway_also: no
switch: on
alarm: off
answer: yes

meeting_time: 1:20
ratio: 12:30:15

version: 1.20
release: 2.0

starts_on: 2026-10-17
starts_at: 2026-10-17T09:30:00

on: push
```

Here is the parser's side of the story —
PyYAML 6.0.3, YAML 1.1 rules, via `show.py`:

```
$ python3 show.py traps.yml
country                              False                        bool
norway_also                          False                        bool
switch                               True                         bool
alarm                                False                        bool
answer                               True                         bool
meeting_time                         80                           int
ratio                                45015                        int
version                              1.2                          float
release                              2.0                          float
starts_on                            datetime.date(2026, 10, 17)  date
starts_at                            datetime.datetime(2026, 10, 17, 9, 30) datetime
True                                 'push'                       str
```

## The Norway problem

`country: NO` was meant as the country code for
Norway. Under YAML 1.1 rules, `NO` is a boolean
spelling — so the value became `False`. A
country dropdown built from parsed data quietly
loses Norway (and, with `ON`/`OFF`-style codes
and words elsewhere, other values besides).

It's a *family* of traps, not one word: `yes`,
`no`, `on`, `off`, `y`, `n` — in any
capitalisation — are booleans to a 1.1 parser.
The whole first block of the table is that
family. Under YAML 1.2 rules they're plain
strings, which is why the same file can be
harmless in one tool and wrong in another.

The last line is the family's most expensive
member: `on: push` was a *key* — the trigger
name in a CI workflow file, say. The key itself
became the boolean `True` (see the table's last
row, where the key column reads `True`). A
program looking for the key `"on"` finds
nothing; the workflow silently never triggers.
This one has bitten a generation of CI users,
because the file looks perfect.

**Defence:** quote anything that must be text —
`country: 'NO'`, `'on': push`, `answer: 'yes'`.
Quoting is absolute; no parser reinterprets a
quoted scalar. And write booleans only as
`true`/`false`, the spellings both rulebooks
share.

## The sexagesimal clock

`meeting_time: 1:20` became the integer **80**.
YAML 1.1 reads `1:20` as a base-60 number —
one "sixty" and twenty ones — a notation meant
for times and angles. `12:30:15` is the same
trick with two colons: 12×3600 + 30×60 + 15 =
45015. Anything shaped like `digits:digits` is
at risk under 1.1 rules: times, ratios, scores,
version-ish strings with a colon in them.

**Defence:** quote times and ratios —
`meeting_time: '1:20'`. Under YAML 1.2 the
notation is gone and the value is a string
anyway (see the table below); quoting makes
the file say the same thing in both.

## The version that loses a digit

`version: 1.20` became the float **1.2**. Three
characters that look like a release number are,
to a parser, a decimal — and decimals don't
keep trailing zeros. `release: 2.0` came back
as the float `2.0`, not the string `"2.0"`. Any
code that compares versions as text, or prints
them back, now has the wrong string.

Unlike Norway, **this one is not a 1.1 quirk**:
a bare `1.20` is a number under YAML 1.2 too.
The cross-parser table below shows both parsers
agreeing on the wrong answer.

**Defence:** quote version numbers, always:
`version: '1.20'`. A version is a label, not a
quantity; nothing real is ever gained by
letting it be a float. (`2.4.1`, with two dots,
is safe unquoted — it's not a valid number, so
parsers leave it a string. `service.yml` relies
on that, and chapter 9's validator checks the
version is still a string, in case an edit ever
makes it `2.4`.)

## Duplicated keys: the silent overwrite

```yaml
service:
  name: beacon
  retries: 2
  retries: 5
```

`duplicate-keys.yml` — the same key twice in
one mapping. The specification says keys should
be unique; most parsers do not check. PyYAML
keeps the **last** value and says nothing:

```
$ python3 -c "import yaml; print(yaml.safe_load(open('duplicate-keys.yml')))"
{'service': {'name': 'beacon', 'retries': 5}}
```

The `retries: 2` line might as well not exist.
In a long config this is how an edit "doesn't
take": you changed the first occurrence; the
program reads the second. A linter catches what
the parser won't — chapter 10 shows yamllint
flagging exactly this file.

## Same file, other rulebook

Here is the whole traps file through yq 4.47.2
(YAML 1.2), printed as JSON:

```
$ yq -o=json '.' traps.yml
{
  "country": "NO",
  "norway_also": "no",
  "switch": "on",
  "alarm": "off",
  "answer": "yes",
  "meeting_time": "1:20",
  "ratio": "12:30:15",
  "version": 1.2,
  "release": 2,
  "starts_on": "2026-10-17",
  "starts_at": "2026-10-17T09:30:00",
  "on": "push"
}
```

Line by line against the PyYAML table: every
boolean trap is a string here, the clock times
are strings, the dates are strings, and the key
is `"on"` again. But `version` is still `1.2`,
and `release` is the number `2`. The 1.2
rulebook fixed the words; it did not — could
not — fix numbers, because `1.20` genuinely is
how you write a number.

The lesson generalises past these two parsers:
**a YAML file's meaning is a joint property of
the file and the parser.** When a value matters,
quote it, and the file means the same thing
everywhere.

## Two loud ones, briefly

Not all traps are silent. Two mistakes produce
errors so reliably that their messages are
decoded in full in chapter 11; meet them here
so you recognise them.

An unquoted `: ` inside a value — the file
`broken-colon.yml` contains
`message: Warning: disk almost full`:

```
yaml.scanner.ScannerError: mapping values are not allowed here
  in "broken-colon.yml", line 5, column 17
```

The parser took the second colon as structure.
Quote the value (or drop the colon) and it
parses.

And a tab used for indentation, in
`broken-tabs.yml`:

```
yaml.scanner.ScannerError: while scanning for the next token
found character '\t' that cannot start any token
  in "broken-tabs.yml", line 6, column 1
```

Tabs are forbidden for indentation, in every
version of the spec, no exceptions. Replace
them with spaces.

Check: `python3 show.py traps.yml` prints
`False` for `country`. If your parser prints
`'NO'` instead, you have a YAML 1.2 parser —
and chapter 8's table tells you which of these
traps you're still exposed to. (The float. The
float is everyone's.)
