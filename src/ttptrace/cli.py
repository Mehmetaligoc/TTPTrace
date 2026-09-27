"""Command-line interface for safe experiment metadata operations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .manifest import ManifestError, load_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ttptrace")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser(
        "validate", help="Validate a TTPTrace experiment manifest"
    )
    validate.add_argument("manifest", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "validate":
        try:
            manifest = load_manifest(args.manifest)
        except (OSError, json.JSONDecodeError, ManifestError) as exc:
            print(f"INVALID: {exc}")
            return 1

        print(
            "VALID: "
            f"{manifest['experiment_id']} "
            f"({manifest['session_type']}, {manifest.get('technique_id') or 'benign'})"
        )
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

