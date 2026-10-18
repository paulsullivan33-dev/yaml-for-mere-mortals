# Multi-Line Strings

Sooner or later a config value is a paragraph:
an embedded script, a message template, a chunk
of SQL. Writing it as one long quoted line is
legal and unreadable. YAML's answer is the
**block scalar**: the value is the indented
text that follows the key, taken whole.

`blocks.yml` holds the same two lines six ways.
Here is what the parser returned for each —
printed with `repr`, so every newline is
visible as `\n` rather than implied:

```
$ python3 -c "
import yaml
d = yaml.safe_load(open('blocks.yml'))
for k, v in d.items():
    print(k, repr(v))
"
literal 'first line\nsecond line\n'
literal_stripped 'first line\nsecond line'
folded 'first line second line\n'
folded_stripped 'first line second line'
keep_the_blanks 'ends with two blank lines\n\n\n'
runbook '#!/bin/sh\n# Restart the checker and tail the log.\nsystemctl restart beacon\ntail -f /var/log/beacon/beacon.log\n'
```

## Literal: `|`

```yaml
literal: |
  first line
  second line
```

The text is kept exactly: line breaks where
they are, indentation beyond the block's own
stripped off. This is the style for anything
where layout is meaning — scripts, commands,
preformatted text. The `runbook` value in the
table is a shell script stored whole: note the
`#` lines inside it are the script's comments,
not YAML's, because inside a block scalar
nothing is YAML any more.

## Folded: `>`

```yaml
folded: >
  first line
  second line
```

Single line breaks are *folded* into spaces;
the paragraph becomes one long line, the way
prose wraps in an editor. (Blank lines inside a
folded block survive as real line breaks — a
folded block of several paragraphs keeps the
paragraph breaks and folds within each.)
This is the style for human prose: messages,
descriptions, licences, anything that will be
re-wrapped by whatever displays it.

## Chomping: the final newline

Both styles above ended with exactly one `\n`.
That's the default, called **clip**: the text
keeps a single trailing newline. Two indicators
change it, appended to the `|` or `>`:

| Indicator | Name | Result for the two lines |
|---|---|---|
| *(none)* | clip | `first line\nsecond line\n` |
| `-` | strip | `first line\nsecond line` |
| `+` | keep | everything, including trailing blank lines |

`literal_stripped` and `folded_stripped` in the
table show strip: no final newline at all.
**Keep** (`|+`) preserves blank lines at the
end of the block instead of discarding them —
`keep_the_blanks` ends with three newlines: its
own line's, plus the two blank lines written
after it in the file.

Which to use: **clip** for almost everything
(most tools expect text to end with one
newline), **strip** when the value is compared
or concatenated and a stray `\n` would poison
it, **keep** almost never — when the trailing
blanks are themselves data.

## Practical notes

- The block's indentation is set by its first
  line; every line must reach at least that
  column or the block ends. A less-indented
  line is how a block scalar stops.
- An explicit indent indicator exists (`|2`),
  for the rare case where the first line is
  itself indented oddly. You'll meet it in
  generated files more than you'll write it.
- A block scalar is one scalar. It contains no
  keys, no lists, no comments for YAML — which
  is exactly why it's the safe place to embed
  scripts and other languages' text.
