# Maps and Lists in Depth

Chapter 2 built a config from mappings, lists,
and scalars. This chapter is about the
combinations — which is to say, about every
real config file — and about YAML's second way
of writing collections: the bracketed **flow
style**, borrowed from JSON.

## Lists of maps

The workhorse shape of configuration: a list
whose items are mappings, one per thing being
configured. From `service.yml`, the three sites
Beacon watches:

```yaml
  targets:
    - name: shop-front
      url: https://shop.example.com/
      expect_status: 200
    - name: api-health
      url: https://api.example.com/health
      expect_status: 200
    - name: blog
      url: https://blog.example.com/
      expect_status: 301
```

The first key of each item rides on the dash
line; the remaining keys align with it, two
spaces past the dash. The parser hands back a
list of three dictionaries, in order:

```
$ python3 -c "import yaml; c = yaml.safe_load(open('service.yml')); [print(t['name'], t['url'], t['expect_status']) for t in c['checks']['targets']]"
shop-front https://shop.example.com/ 200
api-health https://api.example.com/health 200
blog https://blog.example.com/ 301
```

Get the alignment wrong — indent `url` one
space less than `name` — and the item ends at
the dash: the parser either errors or, worse,
quietly gives you a different structure. This is
the shape to be most careful with when editing
by hand, because it's the shape every tool
uses for "a list of things with settings."

## Maps of lists, lists of lists

The other combinations are the same pieces
nested the other way. `alerts.email` in
`service.yml` is a list inside a mapping inside
a mapping. A list can hold lists, too — a
matrix, a grid of coordinates, steps with
substeps:

```
$ python3 -c "import yaml; print(yaml.safe_load('grid:\n  - [1, 2]\n  - [3, 4]'))"
{'grid': [[1, 2], [3, 4]]}
```

Depth is not the risk; consistency is. Any of
these shapes parses the same way at five levels
as at two, provided every level keeps its own
column.

## Flow style

Any collection can be written in one line,
JSON-style: sequences in `[ ]`, mappings in
`{ }`, items separated by commas.

```
$ python3 -c "import yaml; print(yaml.safe_load('ports: [8080, 8443]'))"
{'ports': [8080, 8443]}
$ python3 -c "import yaml; print(yaml.safe_load('{name: beacon, port: 8080}'))"
{'name': 'beacon', 'port': 8080}
```

Flow and block are the same data, and they mix
freely — a flow list as a value inside a block
mapping is the common case, as in the `grid`
example above. Written in block style,
`[8080, 8443]` is:

```
$ python3 -c "import yaml; print(yaml.safe_load('ports:\n  - 8080\n  - 8443'))"
{'ports': [8080, 8443]}
```

Same result. Choose per collection:

- **Flow** for short, leaf collections that read
  as a unit: a pair of ports, a list of tags,
  coordinates, a tiny map of flags. One line,
  no alignment to break.
- **Block** for anything with its own nested
  structure, anything likely to grow, and
  anything a human will edit line by line —
  diffs and comments both work per-line, and
  flow style has neither (a comment inside a
  flow collection ends it, since `#` runs to
  the end of the line).

Two flow-style cautions. Commas are structural
there, so a plain scalar in flow style can't
contain one unquoted. And in flow mappings the
colon needs its space less strictly than in
block style on some parsers — write `{name:
beacon}` with the space anyway; consistency
travels better between parsers than cleverness.

## Empty collections

`[]` and `{}` are values: an empty list and an
empty mapping, distinct from null and from an
absent key. A program can tell "set, but empty"
from "not set" — if you write it that way.

Check: `ports: [8080, 8443]` and its block-style
twin above print the identical dictionary.
Style is for humans; the parser keeps neither.
