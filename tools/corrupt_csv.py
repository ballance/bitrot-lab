#!/usr/bin/env python3
"""
CSV File Corruption Tool
Demonstrates how CSV files can break
"""

import sys
import random
import os

def corrupt_csv_file(filename, corruption_type='missing_comma'):
    """Corrupt a CSV file in various ways"""

    # Read the file
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) == 0:
        print("Error: File is empty!")
        return

    print(f"Original file: {len(lines)} lines")
    print(f"Corruption type: {corruption_type}")

    original_lines = lines.copy()

    # Apply corruption
    if corruption_type == 'missing_comma' or corruption_type == '1':
        # Remove a random comma from a data row
        if len(lines) > 1:
            row_idx = random.randint(1, len(lines) - 1)
            row = lines[row_idx]
            comma_positions = [i for i, c in enumerate(row) if c == ',']
            if comma_positions:
                pos = random.choice(comma_positions)
                lines[row_idx] = row[:pos] + row[pos+1:]
                print(f"Removed comma from line {row_idx + 1}, position {pos}")
                print(f"  Before: {original_lines[row_idx].strip()}")
                print(f"  After:  {lines[row_idx].strip()}")

    elif corruption_type == 'extra_comma' or corruption_type == '2':
        # Add an extra comma
        if len(lines) > 1:
            row_idx = random.randint(1, len(lines) - 1)
            row = lines[row_idx]
            pos = random.randint(0, len(row) - 1)
            lines[row_idx] = row[:pos] + ',' + row[pos:]
            print(f"Added comma to line {row_idx + 1}, position {pos}")
            print(f"  Before: {original_lines[row_idx].strip()}")
            print(f"  After:  {lines[row_idx].strip()}")

    elif corruption_type == 'missing_quote' or corruption_type == '3':
        # Remove a quote character
        quote_found = False
        for row_idx in range(len(lines)):
            if '"' in lines[row_idx]:
                row = lines[row_idx]
                quote_pos = row.index('"')
                lines[row_idx] = row[:quote_pos] + row[quote_pos+1:]
                print(f"Removed quote from line {row_idx + 1}, position {quote_pos}")
                print(f"  Before: {original_lines[row_idx].strip()}")
                print(f"  After:  {lines[row_idx].strip()}")
                quote_found = True
                break
        if not quote_found:
            print("No quotes found in file - skipping this corruption")

    elif corruption_type == 'merge_rows' or corruption_type == '4':
        # Remove a newline to merge two rows
        if len(lines) > 2:
            row_idx = random.randint(1, len(lines) - 2)
            lines[row_idx] = lines[row_idx].rstrip('\n\r') + ' ' + lines[row_idx + 1]
            del lines[row_idx + 1]
            print(f"Merged lines {row_idx + 1} and {row_idx + 2}")
            print(f"  Result: {lines[row_idx].strip()}")

    elif corruption_type == 'wrong_delimiter' or corruption_type == '5':
        # Change commas to semicolons in one row
        if len(lines) > 1:
            row_idx = random.randint(1, len(lines) - 1)
            lines[row_idx] = lines[row_idx].replace(',', ';')
            print(f"Changed commas to semicolons in line {row_idx + 1}")
            print(f"  Before: {original_lines[row_idx].strip()}")
            print(f"  After:  {lines[row_idx].strip()}")

    elif corruption_type == 'duplicate_header' or corruption_type == '6':
        # Insert duplicate header in the middle
        if len(lines) > 1:
            pos = len(lines) // 2
            lines.insert(pos, lines[0])
            print(f"Inserted duplicate header at line {pos + 1}")

    else:
        print(f"Unknown corruption type: {corruption_type}")
        print("Using missing_comma instead...")
        return corrupt_csv_file(filename, 'missing_comma')

    # Write corrupted data back
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\nCorrupted! New file: {len(lines)} lines")
    print(f"File: {filename}")

def show_help():
    print("""
CSV File Corruption Tool

Usage:
    python3 corrupt_csv.py <filename> [corruption_type]

Corruption Types:
    1 or missing_comma   - Remove a comma (default)
    2 or extra_comma     - Add an extra comma
    3 or missing_quote   - Remove a quote character
    4 or merge_rows      - Remove newline to merge rows
    5 or wrong_delimiter - Change commas to semicolons
    6 or duplicate_header - Insert duplicate header

Examples:
    python3 corrupt_csv.py test.csv
    python3 corrupt_csv.py test.csv missing_comma
    python3 corrupt_csv.py test.csv merge_rows

Make a backup before corrupting!
    cp original.csv test.csv
    python3 corrupt_csv.py test.csv
""")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        sys.exit(1)

    corruption_type = sys.argv[2] if len(sys.argv) > 2 else 'missing_comma'

    # Confirm before corrupting
    print(f"About to corrupt: {filename}")
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)

    corrupt_csv_file(filename, corruption_type)
