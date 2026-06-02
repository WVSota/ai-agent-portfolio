"""
CSV -> JSON converter.

Features:
  - Streams large files (constant memory, row-by-row).
  - Optional type inference (int/float/bool/null) per cell.
  - Handles quoted fields, embedded commas/newlines, custom delimiters.
  - Outputs a JSON array or newline-delimited JSON (--ndjson).

Usage:
    python csv_to_json.py input.csv -o out.json
    python csv_to_json.py input.csv --ndjson --no-infer
"""
from __future__ import annotations
import argparse, csv, json, sys
from typing import Any, Iterator


def infer(value: str) -> Any:
    if value == "":
        return None
    low = value.lower()
    if low in ("true", "false"):
        return low == "true"
    if low in ("null", "none", "nan"):
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def rows(path: str, delimiter: str, do_infer: bool) -> Iterator[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            if do_infer:
                row = {k: infer(v) if v is not None else None for k, v in row.items()}
            yield row


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert CSV to JSON.")
    ap.add_argument("input")
    ap.add_argument("-o", "--output", default="-", help="output file or - for stdout")
    ap.add_argument("-d", "--delimiter", default=",")
    ap.add_argument("--ndjson", action="store_true", help="newline-delimited JSON")
    ap.add_argument("--no-infer", dest="infer", action="store_false")
    args = ap.parse_args()

    out = sys.stdout if args.output == "-" else open(args.output, "w", encoding="utf-8")
    try:
        if args.ndjson:
            for row in rows(args.input, args.delimiter, args.infer):
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
        else:
            out.write("[\n")
            first = True
            for row in rows(args.input, args.delimiter, args.infer):
                out.write(("" if first else ",\n") + "  " + json.dumps(row, ensure_ascii=False))
                first = False
            out.write("\n]\n")
    finally:
        if out is not sys.stdout:
            out.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
