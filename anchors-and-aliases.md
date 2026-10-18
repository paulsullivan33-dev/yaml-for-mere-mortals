# Anchors, Aliases and Merges

Real configs repeat themselves: three
environments that differ in one key each, two
checks that differ in one path. Copy-pasting the
shared parts guarantees they'll drift apart.
YAML's answer is to define a value once, tag it
with an **anchor**, and refer to it by **alias**
— and, for mappings, to **merge** it into
another mapping and override what differs.

`anchors.yml` defines a defaults mapping once
and builds three environments from it:

```yaml
defaults: &defaults
  retries: 2
  timeout_seconds: 10
  notify: true
  log_level: info

development:
  <<: *defaults
  log_level: debug

staging:
  <<: *defaults
  timeout_seconds: 20

production:
  <<: *defaults
  retries: 5
  log_level: warn
```

The pieces:

- `&defaults` — an **anchor**: a name for the
  value that follows it. The anchor is attached
  where the value is defined, on the same line
  as its key.
- `*defaults` — an **alias**: a reference to
  the anchored value, usable anywhere a value
  can go.
- `<<` — the **merge key**: "take the mapping
  this alias points at and pour its keys in
  here." Keys written out in the mapping itself
  win over merged ones.

## What the parser hands back

Anchors and aliases are a *writing* device.
They are resolved while parsing, and the
program receives plain data with the shared
parts filled in — this is `show.py` on the
environments:

```
defaults.retries                     2                            int
defaults.timeout_seconds             10                           int
defaults.notify                      True                         bool
defaults.log_level                   'info'                         str
development.retries                  2                            int
development.timeout_seconds          10                           int
development.notify                   True                         bool
development.log_level                'debug'                      str
staging.retries                      2                            int
staging.timeout_seconds              20                           int
staging.notify                       True                         bool
staging.log_level                   'info'                         str
production.retries                   5                            int
production.timeout_seconds           10                           int
production.notify                    True                         bool
production.log_level                   'warn'                         str
```

Read it as the resolution rules made visible:
`development` kept the defaults except
`log_level`, which it overrode to `debug`;
`staging` overrode only `timeout_seconds`;
`production` overrode `retries` and
`log_level` and inherited the other two. And
here is `production` alone, printed as JSON —
no anchors, no merge, just the result:

```
$ python3 -c "import yaml, json; d = yaml.safe_load(open('anchors.yml')); print(json.dumps(d['production'], indent=2))"
{
  "retries": 5,
  "timeout_seconds": 10,
  "notify": true,
  "log_level": "warn"
}
```

Merging works for any mapping, not just
environment blocks — `anchors.yml` builds two
HTTP probes from one anchored probe the same
way, overriding only `path`, and `show.py`
confirms both got the shared `method` and
`expect_status`.

## Aliases for whole values

An alias can stand anywhere a value can,
including as a complete value by itself:

```yaml
oncall: &oncall
  - ops@example.com
  - oncall@example.com

alerts_to: *oncall
```

`alerts_to` *is* `oncall` — in PyYAML, quite
literally the same object in memory:

```
$ python3 -c "import yaml; d = yaml.safe_load(open('anchors.yml')); print(d['alerts_to'] is d['oncall'])"
True
```

For config reading that changes nothing. If a
program *modifies* the data it loaded, though,
a change through one name appears through the
other — worth knowing before it surprises you.

## Merging several anchors

The merge key accepts a list of aliases:

```yaml
child:
  <<: [*b1, *b2]
  c: 5
```

When two merged mappings have the same key, the
**earlier** alias in the list wins — the
opposite of the "later overrides" rule most
people guess:

```
$ python3 -c "
import yaml
s = '''
base1: &b1
  a: 1
  b: 2
base2: &b2
  b: 3
  c: 4
child:
  <<: [*b1, *b2]
  c: 5
'''
print(yaml.safe_load(s)['child'])
"
{'b': 2, 'c': 5, 'a': 1}
```

`b` is 2 (from `base1`, first in the list, not
`base2`'s 3), and the explicit `c: 5` beats both
merges, as explicit keys always do.

## Honest limits

- **The anchor's home is real data too.**
  `defaults` and `probe` in `anchors.yml` are
  ordinary keys; the program receives them
  alongside the environments. Config systems
  that use anchors heavily often park them under
  a key the program ignores (a common convention
  is a name starting with `x-`), but that
  ignoring is the program's business, not
  YAML's.
- **Aliases point backwards.** An anchor must be
  defined earlier in the file than its aliases.
- **Not every parser is obliged to merge.** The
  merge key is part of YAML's core types and
  PyYAML resolves it, as does yq — but a tool
  that reads YAML "simply" may hand you the
  literal `<<` key instead. If a config relies
  on merges, check that its consumer resolves
  them; this is a documented behaviour
  difference, not a bug in your file.
