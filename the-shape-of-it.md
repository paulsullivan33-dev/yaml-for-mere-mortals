# The Shape of It

A YAML file is built from three pieces, combined
without limit:

- a **mapping** — keys with values, like a
  dictionary or an object
- a **sequence** — an ordered list
- a **scalar** — a single value: a string, a
  number, a boolean, or null

The mappings are the look YAML is known for:

```yaml
server:
  host: 0.0.0.0
  port: 8080
```

A key, a colon, a space, a value. When the value
is itself a mapping, it goes on the next lines,
indented. **Indentation is the only structure
there is.** There are no closing braces to count
and no commas to forget; if two keys line up,
they are siblings, and if a line is indented
further than the one above, it belongs to it.

## One file, taken apart

`service.yml` in `examples/` is a complete
config for a fictional uptime monitor called
Beacon. Its top level is six keys:

```
$ python3 -c "import yaml; print(list(yaml.safe_load(open('service.yml'))))"
['service', 'server', 'checks', 'alerts', 'features', 'logging']
```

Every value under those keys is a mapping, a
list, or a scalar, three levels deep at most.
Zoom into one corner:

```
$ python3 -c "import yaml; c = yaml.safe_load(open('service.yml')); print(c['server']['tls'])"
{'enabled': True, 'cert_file': '/etc/beacon/cert.pem', 'key_file': '/etc/beacon/key.pem'}
```

That is what a program receives: the nested
mapping under `server`, then under it `tls`,
then three scalars. When you edit a config you
are editing this shape; the parser rebuilds it
exactly, or refuses with an error.

## Lists

A list is a run of lines starting with a dash
and a space, at the same indentation:

```yaml
email:
  - ops@example.com
  - oncall@example.com
```

The dash is part of the indentation: the items
hang two spaces in from their key. A list item
can itself be a mapping (chapter 4 lives on
this), in which case the first key sits on the
dash line and the rest line up beneath it.

A single scalar can also be a whole document —
a file containing just `beacon` is valid YAML
that parses to one string — but config files are
almost always a mapping at the top.

## Comments

A `#` starts a comment when it begins a token:
at the start of a line, or after whitespace.
The parser drops comments entirely; they are
for the human. The rule matters where there is
no whitespace:

```
$ printf 'name: beacon # the monitor\npath: /var/log/beacon#old\n' | python3 -c "import yaml, sys; print(yaml.safe_load(sys.stdin))"
{'name': 'beacon', 'path': '/var/log/beacon#old'}
```

After a space, `# the monitor` is a comment and
the value is just `beacon`. Glued to the word,
`beacon#old` is the value, `#` and all — a real
way to break a file path or a URL fragment
without noticing. Chapter 5 uses comments inside
a quoted script, where they belong to the text
and not to YAML at all.

## The indentation rules that matter

1. **Spaces, never tabs.** A tab used for
   indentation is an error — a loud one,
   demonstrated in chapter 8.
2. **Siblings line up.** Keys at the same level
   start in the same column. One space deeper
   or shallower and the parser builds a
   different shape or gives up; chapter 11
   decodes the error for the shallower case.
3. **Any consistent width works.** Two spaces is
   the near-universal convention, and every
   example here uses it. Four is legal. The spec
   allows one — legal, and a trap: one-space
   indentation makes the "sibling one space out"
   mistake invisible to the eye. Match the file
   you're editing, and when you start a file,
   use two.

Nothing else about layout is load-bearing: blank
lines are ignored, and a value's line can be as
long as it needs to be (a linter may disagree —
chapter 10).

Check: in `service.yml`, the six top-level keys
print in file order — YAML mappings are ordered,
and parsers keep your order. If your Python
prints them in the same order as the file,
you're seeing what the program sees.
