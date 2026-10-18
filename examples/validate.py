#!/usr/bin/env python3
"""Check a Beacon config file the way the service
would on startup: required keys present, and every
value the type the service expects.

    python3 validate.py service.yml
"""
import sys

import yaml


def check(cond, message):
    print(("ok   " if cond else "FAIL ") + message)
    return cond


def main():
    with open(sys.argv[1]) as fh:
        cfg = yaml.safe_load(fh)
    ok = True
    ok &= check(isinstance(cfg, dict), "top level is a mapping")
    name = cfg["service"]["name"]
    ok &= check(isinstance(name, str),
                f"service.name is a string (got {name!r})")
    version = cfg["service"]["version"]
    ok &= check(isinstance(version, str),
                "service.version is a string "
                f"(got {type(version).__name__})")
    port = cfg["server"]["port"]
    ok &= check(isinstance(port, int) and 1 <= port <= 65535,
                f"server.port is a port number (got {port!r})")
    targets = cfg["checks"]["targets"]
    ok &= check(isinstance(targets, list) and len(targets) > 0,
                "checks.targets is a non-empty list")
    for t in targets:
        status = t["expect_status"]
        ok &= check(isinstance(status, int),
                    f"target {t['name']}: expect_status "
                    f"is an integer (got {status!r})")
    emails = cfg["alerts"]["email"]
    ok &= check(isinstance(emails, list)
                and all(isinstance(e, str) for e in emails),
                "alerts.email is a list of strings")
    print("VALID" if ok else "INVALID")
    return 0 if ok else 1


sys.exit(main())
