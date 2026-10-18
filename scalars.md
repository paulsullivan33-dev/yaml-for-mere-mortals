# Scalars

A scalar is a single value. YAML's defining
habit is that almost nothing in the file is
labelled: you write `8080` and the parser
decides whether that's a number or a string,
using rules called *implicit typing*. This
chapter walks `types.yml`, the sample file with
one of almost everything, through `show.py` —
so every claim below is the parser's answer,
not the documentation's.

```
$ python3 show.py types.yml
plain_string                         'beacon'                     str
single_quoted                        "it's a monitor"             str
double_quoted                        'tab\there'                  str
string_with_colon                    'status: ok'                 str
string_that_looks_like_a_number      '8080'                       str
integer                              8080                         int
negative                             -12                          int
underscored_number                   1000                         int
leading_zero                         48                           int
float                                2.5                          float
float_with_exponent                  1200.0                       float
looks_scientific_but_is_text         '1.2e3'                      str
truthy                               True                         bool
also_truthy                          True                         bool
switched_on                          True                         bool
switched_off                         False                        bool
nothing_here                         None                         NoneType
also_nothing                         None                         NoneType
empty_value                          None                         NoneType
empty_string                         ''                           str
```

## Strings: three styles

**Plain** — no quotes at all: `beacon`. The
default, and the right choice whenever it's
allowed. Plain scalars can't contain `: `
(colon-space) or ` #`, can't start with most
punctuation characters (`-`, `?`, `:` are
structural), and are trimmed of surrounding
spaces.

**Single-quoted** — `'it''s a monitor'`. The
only escape inside single quotes is the quote
itself, doubled. Everything else is literal:
no `\n`, no surprises. This is the style to
reach for when a value must stay exactly as
written — chapter 8's defences live here.

**Double-quoted** — `"tab\there"`. The string
in the table printed as `'tab\there'` because
the parser turned the two characters `\t` into
a real tab, and `repr` shows it as `\t` again.
Double quotes are YAML's escape hatch: `\n`,
`\t`, `\"`, `\uXXXX` and friends all work, as
they do in JSON. If a value needs a colon:
`"status: ok"` — quoted, the `: ` is harmless.

The rule of thumb: plain when you can,
single-quoted when you must force a string,
double-quoted when you need escapes.

## Numbers

The parser hands back integers and floats:

- `8080`, `-12` — integers.
- `1_000` — underscores are allowed as visual
  grouping and ignored: the value is `1000`.
- `060` — **48**. A leading zero makes the
  number octal (base 8) under the YAML 1.1
  rules PyYAML follows. File permissions and
  zero-padded IDs written bare can change value
  in silence; quote them if they're really
  labels.
- `2.5`, `1.` — floats.
- `1.2e+3` — a float, 1200.0. But `1.2e3`,
  without the `+`, is a **string** in PyYAML:
  its number patterns insist on the exponent's
  sign. (`looks_scientific_but_is_text` in the
  table.) Other parsers differ — one more entry
  for the "know your parser" list.
- `.inf` and `.nan` are floats too, YAML's
  spellings of infinity and not-a-number.

Hex (`0x1F` → 31) is recognised; `0o17` is not
— PyYAML reads it as a string, since 1.1 spells
octal with the leading zero above.

## Booleans

`true` and `false` are the spellings every
parser agrees on, and the only ones you should
write. PyYAML, following YAML 1.1, also accepts
`y`, `yes`, `n`, `no`, `on`, `off` and their
capitalisations — `types.yml`'s `yes`, `on`,
and `off` all became booleans in the table.
Under YAML 1.2 rules those same words are
strings. That disagreement is the single most
productive source of YAML bugs in the wild, and
it gets its own chapter (chapter 8). Write
`true` and `false`; quote anything else you
mean as text.

## Null: the spellings of nothing

Three lines in the table all became `None`
(Python's null):

```yaml
nothing_here: null
also_nothing: ~
empty_value:
```

`null`, `~`, and *nothing at all after the
colon* are the same value. A fourth spelling is
an absent key, which most programs also treat
as "not set" — the distinction matters when a
program must tell "explicitly unset" from
"never mentioned," and YAML can only give it
the first three.

Null is **not** the empty string:
`empty_string: ''` is a string of length zero,
a real value a program can print, compare, and
reject differently. "No value" and "empty
value" are different statements, and YAML keeps
them separate if you let it.
