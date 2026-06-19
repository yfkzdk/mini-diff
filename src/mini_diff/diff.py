"""Unified diff engine — simplified LCS + GNU diff format."""

from dataclasses import dataclass


@dataclass
class Hunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list


@dataclass
class DiffResult:
    old_file: str
    new_file: str
    hunks: list


def _longest_common_subsequence(a, b):
    """Simple DP LCS — returns indices of matching lines."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])

    # Backtrack
    matches = []
    i, j = m, n
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            matches.append((i - 1, j - 1))
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return list(reversed(matches))


def compare(old_lines, new_lines, old_file="", new_file=""):
    """Compare two lists of lines, return DiffResult with hunks."""
    if not old_lines and not new_lines:
        return DiffResult(old_file, new_file, [])

    matches = _longest_common_subsequence(old_lines, new_lines)

    if not matches and not old_lines and not new_lines:
        return DiffResult(old_file, new_file, [])

    # Build edit script from LCS
    edits = []  # ('=', old_idx, new_idx) or ('-', old_idx) or ('+', new_idx)
    oi, ni = 0, 0
    for om, nm in matches:
        while oi < om:
            edits.append(("-", oi, None))
            oi += 1
        while ni < nm:
            edits.append(("+", None, ni))
            ni += 1
        edits.append(("=", oi, ni))
        oi += 1
        ni += 1
    while oi < len(old_lines):
        edits.append(("-", oi, None))
        oi += 1
    while ni < len(new_lines):
        edits.append(("+", None, ni))
        ni += 1

    if not edits:
        return DiffResult(old_file, new_file, [])

    # Group into hunks (context = 3 lines)
    hunks = []
    i = 0
    while i < len(edits):
        if edits[i][0] == "=":
            i += 1
            continue
        # Found a change — backtrack for context
        hunk_start = max(0, i - 3)
        # Forward for context
        hunk_end = min(len(edits), i + 1)
        while hunk_end < len(edits) and edits[hunk_end][0] != "=":
            hunk_end += 1
        # Include trailing context
        context_end = min(len(edits), hunk_end + 3)
        while context_end < len(edits) and edits[context_end][0] == "=":
            context_end += 1
            if context_end - hunk_end > 3:
                context_end -= 1
                break

        # Build hunk
        old_start = None
        new_start = None
        old_count = 0
        new_count = 0
        lines = []

        for j in range(hunk_start, context_end):
            op, oidx, nidx = edits[j]
            if op == "=":
                lines.append(" " + old_lines[oidx])
                old_count += 1
                new_count += 1
                if old_start is None:
                    old_start = oidx + 1
                if new_start is None:
                    new_start = nidx + 1
            elif op == "-":
                lines.append("-" + old_lines[oidx])
                old_count += 1
                if old_start is None:
                    old_start = oidx + 1
            elif op == "+":
                lines.append("+" + new_lines[nidx])
                new_count += 1
                if new_start is None:
                    new_start = nidx + 1

        # Fallback for edge case
        if old_start is None:
            old_start = 1
        if new_start is None:
            new_start = 1

        hunks.append(Hunk(old_start, old_count, new_start, new_count, lines))
        i = context_end

    return DiffResult(old_file, new_file, hunks)


def format_unified(result, old_file, new_file):
    """Format DiffResult as unified diff string."""
    if not result.hunks:
        return ""

    out = [f"--- {old_file}", f"+++ {new_file}"]
    for h in result.hunks:
        old_range = f"-{h.old_start},{h.old_count}" if h.old_count != 1 else f"-{h.old_start}"
        new_range = f"+{h.new_start},{h.new_count}" if h.new_count != 1 else f"+{h.new_start}"
        out.append(f"@@ {old_range} {new_range} @@")
        for line in h.lines:
            out.append(line.rstrip("\n"))
    return "\n".join(out) + "\n"
