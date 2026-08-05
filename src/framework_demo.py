from __future__ import annotations

import argparse
import json

VERSION = "0.1.0"


def health() -> dict[str, str]:
    return {"status": "ok", "version": VERSION}


def main() -> None:
    parser = argparse.ArgumentParser(description="DevOps sandbox demo")
    parser.add_argument("command", choices=("health", "version"))
    args = parser.parse_args()

    if args.command == "health":
        print(json.dumps(health(), sort_keys=True))
        return

    print(VERSION)


if __name__ == "__main__":
    main()
