# What YAML Is

YAML is a way of writing structured data as
plain text. A YAML file describes the same kind
of thing a JSON file does — mappings of keys to
values, lists, strings, numbers, booleans, and
nothing — but it is written to be read and
edited by people:

```yaml
service: beacon
port: 8080
features:
  - dashboard
  - alerts
```

That is the whole idea, and also the whole
problem this guide exists to explain: YAML
leaves out the punctuation, so the *parser* has
to work out what you meant — what is structure,
what is text, and what type each value is. It is
very good at this. It is not perfect, and its
mistakes are systematic enough to have names.

## Where you meet it

YAML became the default format for files that
humans configure and machines read:

- CI and automation pipelines, whose steps,
  triggers, and settings live in YAML files
- container and orchestration tooling, which
  describes whole systems in YAML manifests
- static-site generators, whose per-page
  settings ("front matter") are YAML
- test fixtures, data files, and the config of
  a large share of modern command-line tools

If you administer anything built in the last
fifteen years, you already edit YAML. This
guide is about editing it with your eyes open.

## YAML is a specification, not a program

There is no single "YAML" you run. There is a
specification — two in circulation, **YAML 1.1**
(2005) and **YAML 1.2** (2009) — and a parser
library in every language that turns YAML text
into data structures. The two rulebooks agree on
almost everything structural and disagree about
some *values*: most famously, which words count
as booleans. Chapter 8 is built on that
disagreement.

So this guide names its parsers, and labels
their output:

- **PyYAML 6.0.3** — the YAML library for
  Python, and the guide's reference parser. It
  follows the **YAML 1.1** rules. Everything
  unlabelled was parsed with it.
- **yq 4.47.2** — a command-line YAML processor
  (the one by Mike Farah), following the
  **YAML 1.2** core rules. It appears where the
  two rulebooks give different answers.

Check your parser before you trust any example,
here or anywhere else:

```
$ python3 -c "import yaml; print(yaml.__version__)"
6.0.3
```

On your own machine, `pip install pyyaml`
provides both the library and that version
string. The examples in this guide also use a
small shipped script, `show.py`, which loads a
file and prints every value the parser produced
next to its type — the guide's standard way of
asking "what did the parser actually see?"

## JSON is a subset of YAML

Every JSON file is, by design, valid YAML: the
1.2 specification was written so that JSON's
syntax is contained in YAML's. This is not a
slogan; a YAML parser will load a JSON file
without noticing anything unusual. `examples/`
ships one, `data.json`:

```
$ python3 -c "import yaml, json; print(json.dumps(yaml.safe_load(open('data.json')), indent=2))"
{
  "features": [
    "dashboard",
    "alerts"
  ],
  "port": 8080,
  "service": "beacon",
  "tls": {
    "enabled": true
  }
}
```

That output is the YAML parser's result printed
back as JSON, and it is the same data Python's
own JSON parser produces — the two agree
exactly:

```
$ python3 -c "import yaml, json; print(yaml.safe_load(open('data.json')) == json.load(open('data.json')))"
True
```

Two practical consequences. First, any JSON
tool can be used to *inspect* YAML once a
converter has had it — chapter 9 converts a
config to JSON and questions it with jq.
Second, the flow style you'll meet in chapter 4
(`[dashboard, alerts]`, `{enabled: true}`) is
YAML wearing JSON's clothes, and it is legal
anywhere a value is expected.

## What YAML is not

- **Not a programming language.** No loops, no
  conditionals, no arithmetic. Anchors and
  merges (chapter 6) are as close as it gets.
- **Not self-describing about types.** A YAML
  file does not record that `1.20` was meant as
  a version; the parser decides, and chapter 3
  shows its rules.
- **Not forgiving about whitespace.** Tabs are
  forbidden for indentation, and a single
  misplaced space changes the structure. The
  errors this produces are chapter 11.

Check: `python3 show.py types.yml` prints a
table of values with types — `plain_string`,
`integer`, `truthy` and friends — without an
error. If it does, your parser and the samples
agree, and everything from here on will
reproduce.
