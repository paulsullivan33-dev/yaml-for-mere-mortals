# YAML for Mere Mortals

**YAML** is the format your configuration files
are already written in — CI workflows, container
tooling, static-site generators, automation of
every kind. It was designed to be written by
humans: no brackets to balance, no commas to
forget, structure shown by indentation alone.
That friendliness has a price. YAML guesses the
*type* of everything you write, and some of its
guesses are famous: a country code that becomes
`false`, a version number that loses a digit, a
clock time that turns into the number 80.

This guide teaches YAML the way it behaves, not
the way it looks: the structure, the scalars, the
multi-line strings, anchors and merges, and then
the traps — every one of them sprung on a real
parser, so you can watch the value change.

Every parse result, error message, and lint
finding in this guide was captured from a real
tool against the sample files in `examples/`:
PyYAML 6.0.3 (Python's YAML library, which follows
the YAML 1.1 rules), with yq 4.47.2 (a YAML 1.2
parser) brought in for the chapter where the two
rulebooks disagree. Where the rulebooks differ,
the guide says so and labels which parser
produced which output. The broken files are
broken on purpose and say so in their headers.

It assumes you edit text files and have opened a
YAML config before — probably to change one value
and save it nervously. No programming experience
is required; the small Python snippets are there
to *show* you the parser's answer, and each one
is a single command you can copy.

## What this guide covers

- [**What YAML is**](what-yaml-is.md) — a data
  format that became the config default, the
  parser this guide uses, and the proof that
  JSON is YAML
- [**The shape of it**](the-shape-of-it.md) —
  keys and values, nesting by indentation,
  lists, and comments
- [**Scalars**](scalars.md) — the three ways to
  write a string, numbers in their many forms,
  booleans, and the spellings of nothing
- [**Maps and lists in depth**](maps-and-lists.md) —
  nested combinations, and flow style, the
  bracketed shorthand
- [**Multi-line strings**](multiline-strings.md) —
  literal and folded blocks, and the chomping
  indicators that control the final newline
- [**Anchors, aliases and merges**](anchors-and-aliases.md) —
  defining a shape once and reusing it, with
  the parser's resolved output as proof
- [**Documents and types**](documents-and-types.md) —
  several documents in one file, explicit tags,
  and the date that stops being a string
- [**The famous traps**](the-famous-traps.md) —
  Norway, the sexagesimal clock, the vanishing
  version digit, duplicate keys, and the two
  errors everyone meets first
- [**A worked example**](worked-example.md) —
  one service config taken apart, converted to
  JSON, questioned with jq, and validated
- [**Writing and checking YAML**](writing-and-checking.md) —
  generating YAML with a dumper and its quirks,
  linting with yamllint, and loading safely
- [**Troubleshooting**](troubleshooting.md) —
  the parser's error messages decoded one by
  one, and a method for finding the fault
- [**Glossary**](glossary.md) — the terms,
  collected in one place

## What it doesn't cover

Writing your own YAML parser; schemas and
validators beyond the small checker in the worked
example; the configuration systems of any one
tool (each has its own manual and its own
opinion about which YAML features it uses); and
the full YAML specification, which is long,
formal, and — for the corners this guide skips —
genuinely hard to read. The chapters point at
the exits where they exist.

## How to use this guide

Copy `examples/` somewhere, read the first three
chapters with a terminal open, and parse the
sample files as you go. By the worked example
you have the everyday skill. Save the traps
chapter for the day a config value isn't what
you typed — a day that comes for everyone who
edits YAML long enough.
