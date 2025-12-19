from __future__ import annotations

import sys
from typing import List, Tuple


Range = Tuple[int, int]


def parse_ranges_and_integers(text: str) -> tuple[List[Range], List[int]]:
    lines = text.splitlines()

    range_lines: List[str] = []
    integer_lines: List[str] = []

    i = 0
    while i < len(lines) and lines[i].strip() != "":
        range_lines.append(lines[i])
        i += 1

    while i < len(lines) and lines[i].strip() == "":
        i += 1

    while i < len(lines):
        if lines[i].strip() != "":
            integer_lines.append(lines[i])
        i += 1

    ranges: List[Range] = []
    for line in range_lines:
        start_s, end_s = line.split("-", 1)
        start = int(start_s)
        end = int(end_s)
        ranges.append((start, end))

    integers: List[int] = []
    for line in integer_lines:
        integers.append(int(line))

    return ranges, integers


def sort_and_merge_connected_ranges(ranges: List[Range]) -> List[Range]:
    ranges_sorted = sorted(ranges)

    merged: List[Range] = []
    for start, end in ranges_sorted:
        if not merged:
            merged.append((start, end))
        else:
            last_start, last_end = merged[-1]
            if start <= last_end + 1:
                merged[-1] = (last_start, max(last_end, end))
            else:
                merged.append((start, end))

    return merged


def includes_using_binary_search(merged_ranges: List[Range], value: int) -> bool:
    lo = 0
    hi = len(merged_ranges) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        start, end = merged_ranges[mid]

        if value < start:
            hi = mid - 1
        elif value > end:
            lo = mid + 1
        else:
            return True

    return False


def count_integers_in_ranges(merged_ranges: List[Range], integers: List[int]) -> int:
    count = 0
    for value in integers:
        if includes_using_binary_search(merged_ranges, value):
            count += 1
    return count


def main() -> None:
    text = sys.stdin.read()
    ranges, integers = parse_ranges_and_integers(text)
    merged_ranges = sort_and_merge_connected_ranges(ranges)
    count = count_integers_in_ranges(merged_ranges, integers)

    for start, end in merged_ranges:
        print(f"{start}-{end}")
    print()
    print(count)


if __name__ == "__main__":
    main()
