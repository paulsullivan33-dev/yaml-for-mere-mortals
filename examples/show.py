#!/usr/bin/env python3
"""Load a YAML file and print what the parser
actually saw: every scalar value, with its type.
Anchors and merges appear already resolved,
because that is what a program receives.

    python3 show.py traps.yml
"""
import sys

import yaml


def show(value, path):
    if isinstance(value, dict):
        for key, val in value.items():
            child = f"{path}.{key}" if path else str(key)
            show(val, child)
    elif isinstance(value, list):
        for i, val in enumerate(value):
            show(val, f"{path}[{i}]")
    else:
        print(f"{path:36} {value!r:28} {type(value).__name__}")


docs = list(yaml.safe_load_all(open(sys.argv[1])))
for n, doc in enumerate(docs, 1):
    if len(docs) > 1:
        print(f"--- document {n}")
    show(doc, "")
