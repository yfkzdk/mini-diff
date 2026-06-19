"""CLI — unified diff tool."""

from .diff import compare, format_unified


def main():
    import argparse
    p = argparse.ArgumentParser(prog="mini-diff")
    p.add_argument("old_file")
    p.add_argument("new_file")
    args = p.parse_args()

    old = open(args.old_file, encoding="utf-8").readlines()
    new = open(args.new_file, encoding="utf-8").readlines()
    result = compare(old, new, args.old_file, args.new_file)
    print(format_unified(result, args.old_file, args.new_file), end="")


if __name__ == "__main__":
    main()
