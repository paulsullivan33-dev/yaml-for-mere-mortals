# Writing and Checking YAML

So far the parser has been reading. This chapter
is the other direction — programs *writing*
YAML — plus the two habits that keep hand-edited
files honest: linting, and loading safely.

## Generating YAML: the dumper

PyYAML's `safe_dump` turns data back into YAML
text. Feed it a dictionary with one of each
awkward value:

```
$ python3 -c "
import yaml
d = {'service': 'beacon', 'debug': 'yes', 'retries': 2, 'notes': None, 'release': '2026-10-17', 'announcement': 'Beacon 2.4 ships on Friday with a faster checker and fewer false alarms for everyone on the team'}
print(yaml.safe_dump(d), end='')
"
announcement: Beacon 2.4 ships on Friday with a faster checker and fewer false alarms
  for everyone on the team
debug: 'yes'
notes: null
release: '2026-10-17'
retries: 2
service: beacon
```

Four quirks, all visible:

1. **Keys come out sorted.** `announcement`
   before `service`, though the dictionary had
   the opposite order. Sorting is the default;
   it's harmless to parsers and noisy in diffs.
2. **Strings that would re-read as another type
   get quoted.** The string `'yes'` is dumped
   quoted — unquoted, it would come back as a
   boolean. The string `'2026-10-17'` is quoted
   for the same reason: bare, it would return
   as a date. The dumper protects its own
   output; this quoting is the traps of chapter
   8, defended automatically.
3. **Long lines wrap.** The announcement folded
   at 80 columns, with the continuation indented
   — a folded plain scalar that reads back as
   one line with a space where the break was.
   (The wrap width is a setting; the default is
   80.)
4. **Null is spelled `null`**, whatever spelling
   the input used.

Dump a whole parsed file and a fifth quirk
appears — sequences are written flush with
their key, not indented under it:

```
$ python3 -c "
import yaml
d = yaml.safe_load(open('service.yml'))
out = yaml.safe_dump(d)
print('\n'.join(out.splitlines()[:8]))
"
alerts:
  email:
  - ops@example.com
  - oncall@example.com
  repeat_after_minutes: 30
  webhook: https://hooks.example.com/beacon
checks:
  interval_seconds: 60
```

Legal YAML, same data — and a style most
humans wouldn't choose. A dumped file is
machine output; treat it as such.

**Round-tripping** — load, dump, load again —
preserves the data, not the text:

```
$ python3 -c "
import yaml
d = yaml.safe_load(open('service.yml'))
back = yaml.safe_load(yaml.safe_dump(d))
print(back == d)
print(list(back))
"
True
['alerts', 'checks', 'features', 'logging', 'server', 'service']
```

Equal, and reordered. Comments, of course, do
not survive at all: the parser dropped them on
the way in. A config with human comments should
be edited as text, never round-tripped through
a dumper. And if the order matters to your
readers, `sort_keys=False` keeps the file's
order instead:

```
service:
  name: beacon
  version: 2.4.1
  environment: production
```

## Linting: yamllint

A parser checks "is this YAML?" A linter —
**yamllint** (`pip install yamllint`; version
1.38.0 here) — checks "is this *good* YAML by
the rules we chose?" It catches the class of
mistakes parsers forgive. The headline example
is chapter 8's duplicate key:

```
$ yamllint duplicate-keys.yml; echo "[exit $?]"
duplicate-keys.yml
  8:3       error    duplication of key "retries" in mapping  (key-duplicates)

[exit 1]
```

Line 8, column 3, the rule named. Errors fail
the run (exit 1); warnings don't. The shipped
`.yamllint` starts from yamllint's default rules
and adjusts two — line length becomes a
100-column warning, and the `---` document-start
marker isn't required of these fragments. Under
it, watch what gets flagged in perfectly valid
files:

```
$ yamllint -c .yamllint service.yml traps.yml; echo "[exit $?]"
service.yml
  44:16     warning  truthy value should be one of [false, true]  (truthy)

traps.yml
  5:10      warning  truthy value should be one of [false, true]  (truthy)
  6:14      warning  truthy value should be one of [false, true]  (truthy)
  7:9       warning  truthy value should be one of [false, true]  (truthy)
  8:8       warning  truthy value should be one of [false, true]  (truthy)
  9:9       warning  truthy value should be one of [false, true]  (truthy)
  20:1      warning  truthy value should be one of [false, true]  (truthy)
[exit 0]
```

The `truthy` rule is the Norway problem as a
lint rule: it warns on every 1.1-only boolean
spelling — `service.yml` line 44 is the
`beta_checks: off` from chapter 9 — while
passing the file, because warnings are advice.
Run yamllint in your editor or your pipeline
and the loudest YAML traps become somebody
else's job to catch. yamllint also reports the
broken files' syntax errors (chapter 11 shows
two), in the same one-line format.

## Loading safely

YAML's full type system can describe program
objects, not just data — and some loaders will
*build* them. In Python this is concrete. Watch
what the unsafe loader does with a two-line
"config":

```
$ python3 -c "import yaml; print(yaml.unsafe_load('x: !!python/object/apply:os.system [\"echo this command ran\"]'))"
this command ran
{'x': 0}
```

The text `this command ran` was printed by a
shell command embedded in the YAML. The value
that came back, `0`, is that command's exit
status. The file didn't describe data; it
described an action, and the loader performed
it. With a different command in place of `echo`,
loading an untrusted config is running
untrusted code — this is a real, named class of
vulnerability, not a curiosity.

The safe loader refuses the same input:

```
yaml.constructor.ConstructorError: could not determine a constructor for the tag 'tag:yaml.org,2002:python/object/apply:os.system'
```

The rules are short enough to memorise:

- **Always `yaml.safe_load`** (or your language's
  equivalent). It builds only strings, numbers,
  booleans, lists, mappings, and standard types.
- **Never** `unsafe_load`, `Loader=yaml.Loader`,
  or their kin on a file you didn't write — and
  treat config files from the internet as
  untrusted input, because they are.
- PyYAML 6 enforces part of this for you: the
  old bare `yaml.load(text)` now refuses to run
  at all —

```
$ python3 -c "import yaml; yaml.load('service: beacon')"
TypeError: load() missing 1 required positional argument: 'Loader'
```

— which is the library insisting you say, out
loud, how much power you're handing the file.
Choose the safe one.
