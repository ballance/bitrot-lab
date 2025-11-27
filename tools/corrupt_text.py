#!/usr/bin/env python3
"""
Text File Corruption Tool
Demonstrates various ways text files can become corrupted
"""

import sys
import random
import os

def corrupt_text_file(filename, corruption_type='random'):
    """Corrupt a text file in various ways"""

    # Read the file
    with open(filename, 'rb') as f:
        data = bytearray(f.read())

    if len(data) == 0:
        print("Error: File is empty!")
        return

    print(f"Original file size: {len(data)} bytes")
    print(f"Corruption type: {corruption_type}")

    # Apply corruption based on type
    if corruption_type == 'random' or corruption_type == '1':
        # Flip random bits
        num_corruptions = random.randint(1, 5)
        print(f"Flipping {num_corruptions} random bytes...")
        for _ in range(num_corruptions):
            pos = random.randint(0, len(data) - 1)
            old_byte = data[pos]
            data[pos] = random.randint(0, 255)
            print(f"  Position {pos}: 0x{old_byte:02X} -> 0x{data[pos]:02X}")

    elif corruption_type == 'encoding' or corruption_type == '2':
        # Insert invalid UTF-8 sequences
        print("Inserting invalid UTF-8 bytes...")
        pos = len(data) // 2
        # Insert a lone continuation byte (invalid)
        data.insert(pos, 0x80)
        print(f"  Inserted 0x80 at position {pos}")

    elif corruption_type == 'truncate' or corruption_type == '3':
        # Remove the last 20%
        new_size = int(len(data) * 0.8)
        data = data[:new_size]
        print(f"Truncated file to {new_size} bytes")

    elif corruption_type == 'line_endings' or corruption_type == '4':
        # Corrupt line endings
        print("Removing random newline characters...")
        newline_positions = [i for i, b in enumerate(data) if b == 0x0A]
        if newline_positions:
            pos = random.choice(newline_positions)
            del data[pos]
            print(f"  Removed newline at position {pos}")

    elif corruption_type == 'header' or corruption_type == '5':
        # Corrupt the beginning of the file
        print("Corrupting first 10 bytes...")
        for i in range(min(10, len(data))):
            old_byte = data[i]
            data[i] = random.randint(0, 255)
            print(f"  Position {i}: 0x{old_byte:02X} -> 0x{data[i]:02X}")

    else:
        print(f"Unknown corruption type: {corruption_type}")
        print("Using random corruption instead...")
        return corrupt_text_file(filename, 'random')

    # Write corrupted data back
    with open(filename, 'wb') as f:
        f.write(data)

    print(f"\nCorrupted! New file size: {len(data)} bytes")
    print(f"File: {filename}")

def show_help():
    print("""
Text File Corruption Tool

Usage:
    python3 corrupt_text.py <filename> [corruption_type]

Corruption Types:
    1 or random      - Flip random bytes (default)
    2 or encoding    - Insert invalid UTF-8 sequences
    3 or truncate    - Remove last 20% of file
    4 or line_endings - Remove random newlines
    5 or header      - Corrupt first 10 bytes

Examples:
    python3 corrupt_text.py test.txt
    python3 corrupt_text.py test.txt random
    python3 corrupt_text.py test.txt encoding

Make a backup before corrupting!
    cp original.txt test.txt
    python3 corrupt_text.py test.txt
""")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        sys.exit(1)

    corruption_type = sys.argv[2] if len(sys.argv) > 2 else 'random'

    # Confirm before corrupting
    print(f"About to corrupt: {filename}")
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)

    corrupt_text_file(filename, corruption_type)
