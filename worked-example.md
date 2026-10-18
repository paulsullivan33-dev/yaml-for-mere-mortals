# A Worked Example

Everything so far, applied to one file:
`service.yml`, the Beacon config from chapter 2.
This chapter takes it apart the way you'd work
on a real config — read it, convert it, ask it
questions, and check it the way the program
will.

## The file, in sections

```yaml
service:
  name: beacon
  version: 2.4.1
  environment: production

server:
  host: 0.0.0.0
  port: 8080
  workers: 4
  tls:
    enabled: true
    cert_file: /etc/beacon/cert.pem
    key_file: /etc/beacon/key.pem
```

Two mappings of plain scalars. Note the quiet
decisions: `version: 2.4.1` is a string because
`2.4.1` is not a number (two dots) — chapter 8
showed what `2.4` would have risked. `host:
0.0.0.0` is a string for the same reason. The
booleans are written `true`/`false`, the
spellings every parser shares.

```yaml
checks:
  interval_seconds: 60
  timeout_seconds: 10
  retries: 2
  targets:
    - name: shop-front
      url: https://shop.example.com/
      expect_status: 200
    ...
```

The list of maps from chapter 4. The URLs are
plain scalars that contain `:` but never `: ` —
`https://` is safe unquoted, which is why the
colon rule (chapter 8) so rarely bites URLs.

```yaml
features:
  dashboard: true
  public_status_page: false
  beta_checks: off
```

And here the file walks into chapter 8 on
purpose: `beta_checks: off` parses — under
PyYAML — as the boolean `False`, which is what
the author meant. `show.py` confirms all three:

```
features.dashboard                   True                         bool
features.public_status_page          False                        bool
features.beta_checks                   False                        bool
```

It works, and it's still the file's weakest
line: under a YAML 1.2 parser `off` is the
*string* `"off"`, and a program testing
truthiness may treat a non-empty string as
enabled. `false` would say the same thing in
every parser. (Chapter 10's linter flags this
exact line.)

## Convert it, then ask it questions

Because JSON is a subset of YAML, any YAML can
be converted to JSON and handed to JSON tools.
With yq:

```
$ yq -o=json '.' service.yml | head -20
{
  "service": {
    "name": "beacon",
    "version": "2.4.1",
    "environment": "production"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "workers": 4,
    "tls": {
      "enabled": true,
      "cert_file": "/etc/beacon/cert.pem",
      "key_file": "/etc/beacon/key.pem"
    }
  },
```

(The `head -20` trims it; the conversion itself
is whole.) From there, jq — the subject of this
series' previous guide — can interrogate it:

```
$ yq -o=json '.' service.yml | jq '.checks.targets[] | "\(.name) expects \(.expect_status)"'
"shop-front expects 200"
"api-health expects 200"
"blog expects 301"
$ yq -o=json '.' service.yml | jq '[.checks.targets[].expect_status] | unique'
[
  200,
  301
]
```

Conversion is also the cheapest sanity check
there is: a file that converts has a structure,
and the JSON view shows it without YAML's
ambiguities — quotes on every string, types
unmistakable.

## Validate it like the program will

Parsing proves the file is YAML. It does not
prove the *config* is right: a port of
`eighty` is perfectly good YAML (a string) and
a broken config. `validate.py`, shipped in
`examples/`, checks the file the way the
service would — required pieces present, each
the type the service expects:

```
$ python3 validate.py service.yml; echo "[exit $?]"
ok   top level is a mapping
ok   service.name is a string (got 'beacon')
ok   service.version is a string (got str)
ok   server.port is a port number (got 8080)
ok   checks.targets is a non-empty list
ok   target shop-front: expect_status is an integer (got 200)
ok   target api-health: expect_status is an integer (got 200)
ok   target blog: expect_status is an integer (got 301)
ok   alerts.email is a list of strings
VALID
[exit 0]
```

Note `service.version is a string` among the
checks: that line exists because of chapter 8.
If an edit ever turns the version into a bare
`2.4`, the parser would hand over a float and
this check — not the parser — is what would say
so.

Now break one value in a scratch copy —
`port: 8080` becomes `port: eighty`:

```
$ sed 's/port: 8080/port: eighty/' service.yml > service-broken.yml
$ python3 validate.py service-broken.yml; echo "[exit $?]"
ok   top level is a mapping
ok   service.name is a string (got 'beacon')
ok   service.version is a string (got str)
FAIL server.port is a port number (got 'eighty')
ok   checks.targets is a non-empty list
ok   target shop-front: expect_status is an integer (got 200)
ok   target api-health: expect_status is an integer (got 200)
ok   target blog: expect_status is an integer (got 301)
ok   alerts.email is a list of strings
INVALID
[exit 1]
```

The parse never failed; the *validation* did,
by name, with the offending value printed.
That's the division of labour to aim for in
your own tooling: YAML's parser for syntax, a
checker for meaning, and a non-zero exit so a
script — or a deployment pipeline — can tell
the difference.

Check: the unmodified `service.yml` validates
VALID with exit 0. Anything else means the file
on disk isn't the file this chapter describes.
