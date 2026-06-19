"""Tests for mini-diff — unified diff output."""

from mini_diff.diff import compare, format_unified


class TestCompare:
    def test_identical(self):
        result = compare(["a\n", "b\n"], ["a\n", "b\n"])
        assert len(result.hunks) == 0

    def test_add_line(self):
        result = compare(["a\n"], ["a\n", "b\n"])
        assert len(result.hunks) == 1
        hunk = result.hunks[0]
        assert hunk.old_start >= 1
        assert any(l.startswith("+") for l in hunk.lines)

    def test_delete_line(self):
        result = compare(["a\n", "b\n"], ["a\n"])
        assert len(result.hunks) == 1
        assert any(l.startswith("-") for l in result.hunks[0].lines)

    def test_modify_line(self):
        result = compare(["a\n"], ["b\n"])
        assert len(result.hunks) == 1
        lines = result.hunks[0].lines
        assert any(l.startswith("-") for l in lines)
        assert any(l.startswith("+") for l in lines)

    def test_empty_files(self):
        result = compare([], [])
        assert len(result.hunks) == 0


class TestFormat:
    def test_unified_output(self):
        result = compare(["old\n"], ["new\n"])
        output = format_unified(result, "old.txt", "new.txt")
        assert "--- old.txt" in output
        assert "+++ new.txt" in output
        assert "@@" in output
        assert "-old" in output
        assert "+new" in output

    def test_identical_no_output(self):
        result = compare(["same\n"], ["same\n"])
        output = format_unified(result, "a.txt", "b.txt")
        assert output == ""
