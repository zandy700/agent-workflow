#!/usr/bin/env python3
"""Load shared rules through Cursor's documented sessionStart hook."""
import json
from pathlib import Path


def main():
    rules = Path(__file__).with_name("USER_RULES.md").read_text(encoding="utf-8")
    print(json.dumps({"additional_context": rules}))


if __name__ == "__main__":
    main()
