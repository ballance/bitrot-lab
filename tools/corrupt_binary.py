#!/usr/bin/env python3
"""
Binary File Corruption Tool
Demonstrates how binary files (images, etc.) can break
"""

import sys
import random
import os

def corrupt_binary_file(filename, corruption_type='corrupt_header'):
    """Corrupt a binary file in various ways"""

    # Read the file
    with open(filename, 'rb') as f:
        data = bytearray(f.read())

    if len(data) == 0:
        print("Error: File is empty!")
        return

    print(f"Original file size: {len(data)} bytes")
    print(f"File signature: {data[:8].hex()}")
    print(f"Corruption type: {corruption_type}")

    # Detect file type
    file_type = "unknown"
    if data[:8] == bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]):
        file_type = "PNG"
    elif data[:2] == bytes([0xFF, 0xD8]):
        file_type = "JPEG"
    elif data[:2] == bytes([0x42, 0x4D]):
        file_type = "BMP"
    elif data[:4] == bytes([0x47, 0x49, 0x46, 0x38]):
        file_type = "GIF"
    elif data[:4] == bytes([0x50, 0x4B, 0x03, 0x04]):
        file_type = "ZIP"

    print(f"Detected file type: {file_type}")

    # Apply corruption
    if corruption_type == 'corrupt_header' or corruption_type == '1':
        # Corrupt the magic number
        print("Corrupting file signature (magic number)...")
        print(f"  Before: {data[:8].hex()}")
        data[0] = data[0] ^ 0x01  # Flip one bit
        print(f"  After:  {data[:8].hex()}")

    elif corruption_type == 'glitch' or corruption_type == '2':
        # Corrupt random bytes in the middle (glitch art effect)
        num_corruptions = random.randint(50, 200)
        print(f"Creating glitch effect ({num_corruptions} bytes)...")

        # Corrupt middle section only
        start = len(data) // 4
        end = len(data) * 3 // 4

        for _ in range(num_corruptions):
            pos = random.randint(start, end)
            data[pos] = random.randint(0, 255)

    elif corruption_type == 'truncate' or corruption_type == '3':
        # Remove the end of the file
        percent = random.randint(10, 40)
        new_size = int(len(data) * (100 - percent) / 100)
        data = data[:new_size]
        print(f"Truncated file by {percent}% to {new_size} bytes")

    elif corruption_type == 'bit_flip' or corruption_type == '4':
        # Flip random individual bits (subtle corruption)
        num_flips = random.randint(10, 50)
        print(f"Flipping {num_flips} random bits...")
        for _ in range(num_flips):
            byte_pos = random.randint(0, len(data) - 1)
            bit_pos = random.randint(0, 7)
            old_byte = data[byte_pos]
            data[byte_pos] ^= (1 << bit_pos)
            print(f"  Byte {byte_pos}, bit {bit_pos}: 0x{old_byte:02X} -> 0x{data[byte_pos]:02X}")

    elif corruption_type == 'insert_data' or corruption_type == '5':
        # Insert random data in the middle
        num_bytes = random.randint(100, 500)
        pos = len(data) // 2
        random_data = bytes([random.randint(0, 255) for _ in range(num_bytes)])
        data[pos:pos] = random_data
        print(f"Inserted {num_bytes} random bytes at position {pos}")

    elif corruption_type == 'swap_bytes' or corruption_type == '6':
        # Swap two sections of data
        section_size = min(1000, len(data) // 4)
        pos1 = random.randint(0, len(data) - section_size - 1)
        pos2 = random.randint(0, len(data) - section_size - 1)

        section1 = data[pos1:pos1 + section_size]
        section2 = data[pos2:pos2 + section_size]

        data[pos1:pos1 + section_size] = section2
        data[pos2:pos2 + section_size] = section1

        print(f"Swapped {section_size} bytes from position {pos1} with position {pos2}")

    else:
        print(f"Unknown corruption type: {corruption_type}")
        print("Using corrupt_header instead...")
        return corrupt_binary_file(filename, 'corrupt_header')

    # Write corrupted data back
    with open(filename, 'wb') as f:
        f.write(data)

    print(f"\nCorrupted! New file size: {len(data)} bytes")
    print(f"File: {filename}")

def show_help():
    print("""
Binary File Corruption Tool

Usage:
    python3 corrupt_binary.py <filename> [corruption_type]

Corruption Types:
    1 or corrupt_header - Corrupt file signature/magic number (default)
    2 or glitch        - Create glitch art effect (random middle bytes)
    3 or truncate      - Remove 10-40% from end
    4 or bit_flip      - Flip individual bits
    5 or insert_data   - Insert random data in middle
    6 or swap_bytes    - Swap two sections

Examples:
    python3 corrupt_binary.py image.png
    python3 corrupt_binary.py image.png glitch
    python3 corrupt_binary.py image.png corrupt_header

Make a backup before corrupting!
    cp original.png test.png
    python3 corrupt_binary.py test.png glitch
    open test.png  # See the glitch effect!
""")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        sys.exit(1)

    corruption_type = sys.argv[2] if len(sys.argv) > 2 else 'corrupt_header'

    # Confirm before corrupting
    print(f"About to corrupt: {filename}")
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)

    corrupt_binary_file(filename, corruption_type)
