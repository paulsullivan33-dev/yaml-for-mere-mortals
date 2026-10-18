# Documents and Types

A YAML file can hold more than one **document**.
A document is one complete value — usually one
mapping — and documents are separated by a line
containing only `---`. `documents.yml` ships
three: a release, its rollout, and a sign-off
for the same version.

```yaml
---
kind: release
version: 2.4.1
date: 2026-10-17
notes: Bug fixes and a faster checker.
---
kind: rollout
...
```

The first `---` at the top of the file is
optional (a lone document is the common case),
but once a file has two documents, the
separator between them is not. A line of `...`
alone marks a document's end explicitly;
PyYAML still expects `---` before the next one
begins — feeding it more content directly is an
error ("expected '<document start>'"), which we
verified rather than assumed.

## Loading more than one

The singular loader refuses a multi-document
file, with a precise complaint:

```
yaml.composer.ComposerError: expected a single document in the stream
  in "documents.yml", line 4, column 1
but found another document
  in "documents.yml", line 8, column 1
```

The plural loader iterates them:

```
$ python3 -c "import yaml; docs = list(yaml.safe_load_all(open('documents.yml'))); print(len(docs)); [print(d['kind']) for d in docs]"
3
release
rollout
signoff
```

Multi-document files are how some tools pack
many small configs into one file — each
document complete, each loaded in turn. If a
file you didn't write fails to load with that
ComposerError, this is why: use the `_all`
loader (or the tool's equivalent) and handle a
list of results.

## What came back: a date that isn't a string

`show.py` on the documents file — look at the
release document's third line:

```
--- document 1
kind                                 'release'                    str
version                              '2.4.1'                      str
date                                 datetime.date(2026, 10, 17)  date
notes                                'Bug fixes and a faster checker.' str
```

`date: 2026-10-17` was not handed back as the
string `"2026-10-17"`. PyYAML recognised the
shape as a timestamp and built a Python `date`
object — and a full timestamp, `2026-10-17T09:30:00`,
becomes a `datetime`. The file didn't say to
do that; the parser's timestamp rule did.

Whether this is a feature or a trap depends on
the program: code expecting a date gets one,
ready-made; code expecting a string gets an
object that formats differently, compares
differently, and breaks in places strings
don't. And it is parser-dependent: yq, the
YAML 1.2 parser, hands timestamps back as
strings (chapter 8 shows both side by side).
If the value must be text, quote it:
`date: "2026-10-17"` is a string in every
parser.

## Tags: saying the type out loud

Implicit typing can be overridden with an
explicit **tag** — `!!str`, `!!int`, and
friends, written before the value:

```
$ python3 -c "import yaml; print(yaml.safe_load('port: !!str 8080'))"
{'port': '8080'}
$ python3 -c "import yaml; print(yaml.safe_load('port: !!int \"8080\"'))"
{'port': 8080}
```

`!!str 8080` forces the digits to be text;
`!!int "8080"` forces quoted text to be a
number. Tags are the emergency override, not
the everyday tool — quoting (chapter 3) covers
nearly every real case with less ceremony. But
knowing tags exist explains two things you'll
meet in the wild: generated YAML sometimes
carries them, and error messages talk about
them.

A tag the parser doesn't know is refused by
the safe loader, by name:

```
yaml.constructor.ConstructorError: could not determine a constructor for the tag '!custom'
  in "<unicode string>", line 1, column 4:
    x: !custom 1
       ^
```

That refusal is a safety property, and chapter
10 is about its big sibling: tags that ask the
parser to build arbitrary program objects.
