# Troubleshooting

When YAML refuses a file, it tells you why —
in a dialect that takes one chapter to learn.
Every error below is the tail of a real
traceback from parsing one of the shipped
broken files with PyYAML 6.0.3. (The traceback
above the tail is Python plumbing; the parser's
own words are at the end. Read errors from the
bottom up.)

## "mapping values are not allowed here"

```
yaml.scanner.ScannerError: mapping values are not allowed here
  in "broken-colon.yml", line 5, column 17
```

**What it means:** the parser was reading a
plain scalar as a *value* and met a second `:`
— which in YAML starts a new mapping. Column 17
is the second colon, the one inside the text.

**Usual cause:** an unquoted value containing
`: ` — a message, a title, a Windows-style
path, a time written into a description.

**Fix:** quote the value.

```
$ printf 'message: "Warning: disk almost full"\n' | python3 -c "import yaml, sys; print(yaml.safe_load(sys.stdin))"
{'message': 'Warning: disk almost full'}
```

This is the most common YAML error in the
world, and the message names everything except
the problem. Now you know its name.

## "found character '\t' that cannot start any token"

```
yaml.scanner.ScannerError: while scanning for the next token
found character '\t' that cannot start any token
  in "broken-tabs.yml", line 6, column 1
```

**What it means:** a tab. The parser is blunt
here because the rule is absolute — tabs may
not be used for indentation.

**Fix:** replace the tab with spaces, then hunt
the source: an editor set to "tabs", a paste
from a web page, a here-doc. If your editor can
show whitespace, turn it on for YAML files; the
tab is invisible otherwise. Note the error says
nothing about indentation — a tab anywhere a
token starts earns the same message.

## "expected <block end>, but found '<block mapping start>'"

```
yaml.parser.ParserError: while parsing a block mapping
  in "broken-indent.yml", line 4, column 1
expected <block end>, but found '<block mapping start>'
  in "broken-indent.yml", line 6, column 2
```

**What it means:** a mapping ended earlier than
the file thinks it did. Two positions are
given: where the mapping started (line 4 — the
`server:` block) and where the parser gave up
(line 6 — `port`, indented one space *less*
than its sibling `host`). The dedent told the
parser "this block is over"; the colon on the
same line told it "a new mapping is starting";
both can't be true.

**Fix:** line the siblings up. One space is
enough to cause it, and at small indents one
space is hard to see — count columns, or let
the editor's indentation guides show you.

## "could not find expected ':'"

```
yaml.scanner.ScannerError: while scanning a simple key
  in "broken-stray.yml", line 6, column 1
could not find expected ':'
  in "broken-stray.yml", line 7, column 1
```

**What it means:** the parser read a line as a
potential *key* and then never found its colon.
Line 6 is the stray line itself, `just a stray
line`; line 7, column 1 — where the error is
pinned — is simply where the parser ran out of
file while still hoping for the colon.

**Usual cause:** a line of prose left in the
file by an edit: a forgotten note, half a
deleted key, a comment that lost its `#`.

**Fix:** delete the stray line, or give it its
`#` back. When this message points *past* your
last real line, believe it: the fault is the
line above the pointer.

## When there's no error at all

The harder class: the file parses and the
values are wrong. That's chapter 8 — the traps
are silent by design. The tools for it are the
ones from the worked example: `show.py` to see
types, conversion to JSON to see structure,
`validate.py`-style checks to enforce meaning.

## A working method

1. **Read the last lines first.** The parser's
   message and its `in "file", line N, column M`
   pointers are at the bottom of the traceback.
2. **Trust both positions.** Many errors carry
   two: where the construct started and where
   the parser gave up. The fault is usually at
   the second; the context is at the first.
3. **Make it smaller.** Copy the file, delete
   half, re-parse. The half that still fails
   holds the fault. Repeat until the failing
   file fits on a screen — YAML errors are
   almost always visible once the file is small.
4. **Fix one thing, re-parse.** Error positions
   move as you fix; the parser reports the
   *first* problem it cannot pass, not every
   problem.
5. **Convert to see structure.** Once a fixed
   file parses, look at what the parser built —
   here, the indent fix for `broken-indent.yml`
   applied by `sed`, parsed and printed as JSON:

```
$ sed 's/ port: 8080/  port: 8080/' broken-indent.yml | python3 -c "import yaml, sys, json; print(json.dumps(yaml.safe_load(sys.stdin), indent=2))"
{
  "server": {
    "host": "beacon.internal",
    "port": 8080
  }
}
```

6. **Get a second opinion.** yamllint reports
   the same syntax faults in a single line each,
   with its own wording — sometimes the clearer
   one:

```
$ yamllint -c .yamllint broken-indent.yml broken-stray.yml
broken-indent.yml
  6:2       error    syntax error: expected <block end>, but found '<block mapping start>' (syntax)

broken-stray.yml
  7:1       error    syntax error: could not find expected ':' (syntax)
```

Two parsers agreeing on a position is about as
located as a fault gets.
