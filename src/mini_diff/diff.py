"""Unified diff engine — stub."""

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


def compare(old_lines, new_lines):
    return DiffResult("", "", [])


def format_unified(result, old_file, new_file):
    return ""
