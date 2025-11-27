#!/usr/bin/env python3
"""
DOCX File Corruption Tool
Demonstrates how DOCX (ZIP-based) files can break
"""

import sys
import random
import os
import shutil

def corrupt_docx_file(filename, corruption_type='zip_header'):
    """Corrupt a DOCX file in various ways"""

    # Read the file
    with open(filename, 'rb') as f:
        data = bytearray(f.read())

    if len(data) == 0:
        print("Error: File is empty!")
        return

    print(f"Original file size: {len(data)} bytes")
    print(f"Corruption type: {corruption_type}")

    # Check if it's a valid ZIP file
    if not data.startswith(b'\x50\x4B\x03\x04'):
        print("Warning: File doesn't start with ZIP signature (PK..)")
        print(f"First 4 bytes: {data[:4].hex()}")

    # Apply corruption
    if corruption_type == 'zip_header' or corruption_type == '1':
        # Corrupt the ZIP signature
        print("Corrupting ZIP signature (first 4 bytes)...")
        print(f"  Before: {data[:4].hex()} (PK..)")
        data[0] = 0x51  # Change P to Q
        print(f"  After:  {data[:4].hex()}")

    elif corruption_type == 'random_bytes' or corruption_type == '2':
        # Flip random bytes in the middle
        num_corruptions = random.randint(5, 10)
        print(f"Flipping {num_corruptions} random bytes...")
        for _ in range(num_corruptions):
            pos = random.randint(100, len(data) - 100)
            old_byte = data[pos]
            data[pos] = random.randint(0, 255)
            print(f"  Position {pos}: 0x{old_byte:02X} -> 0x{data[pos]:02X}")

    elif corruption_type == 'truncate' or corruption_type == '3':
        # Remove the last 10%
        new_size = int(len(data) * 0.9)
        data = data[:new_size]
        print(f"Truncated file to {new_size} bytes (removed {len(data) - new_size} bytes)")

    elif corruption_type == 'xml' or corruption_type == '4':
        # Extract, corrupt XML, repack
        print("Extracting DOCX to modify XML...")
        import zipfile
        import tempfile

        temp_dir = tempfile.mkdtemp()
        try:
            # Extract
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Corrupt document.xml if it exists
            doc_xml_path = os.path.join(temp_dir, 'word', 'document.xml')
            if os.path.exists(doc_xml_path):
                with open(doc_xml_path, 'r', encoding='utf-8') as f:
                    xml_content = f.read()

                # Remove a random closing tag
                import re
                closing_tags = re.findall(r'</[^>]+>', xml_content)
                if closing_tags:
                    tag_to_remove = random.choice(closing_tags)
                    xml_content = xml_content.replace(tag_to_remove, '', 1)
                    print(f"Removed XML tag: {tag_to_remove}")

                with open(doc_xml_path, 'w', encoding='utf-8') as f:
                    f.write(xml_content)

                # Repack
                print("Repacking DOCX...")
                with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zip_ref.write(file_path, arcname)

                print("Done! XML corrupted and file repacked.")
                return
            else:
                print("document.xml not found in archive")

        finally:
            shutil.rmtree(temp_dir)

    elif corruption_type == 'delete_file' or corruption_type == '5':
        # Extract, delete a file, repack
        print("Extracting DOCX to remove internal file...")
        import zipfile
        import tempfile

        temp_dir = tempfile.mkdtemp()
        try:
            # Extract
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Delete _rels directory
            rels_path = os.path.join(temp_dir, '_rels')
            if os.path.exists(rels_path):
                shutil.rmtree(rels_path)
                print("Deleted _rels directory")

                # Repack
                print("Repacking DOCX...")
                with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zip_ref.write(file_path, arcname)

                print("Done! Relationships removed and file repacked.")
                return

        finally:
            shutil.rmtree(temp_dir)

    else:
        print(f"Unknown corruption type: {corruption_type}")
        print("Using zip_header instead...")
        return corrupt_docx_file(filename, 'zip_header')

    # Write corrupted data back (for non-ZIP manipulations)
    if corruption_type in ['zip_header', 'random_bytes', 'truncate', '1', '2', '3']:
        with open(filename, 'wb') as f:
            f.write(data)

        print(f"\nCorrupted! New file size: {len(data)} bytes")
        print(f"File: {filename}")

def show_help():
    print("""
DOCX File Corruption Tool

Usage:
    python3 corrupt_docx.py <filename> [corruption_type]

Corruption Types:
    1 or zip_header    - Corrupt ZIP signature (default)
    2 or random_bytes  - Flip random bytes
    3 or truncate      - Remove last 10%
    4 or xml           - Corrupt internal XML structure
    5 or delete_file   - Remove _rels directory

Examples:
    python3 corrupt_docx.py test.docx
    python3 corrupt_docx.py test.docx zip_header
    python3 corrupt_docx.py test.docx xml

Make a backup before corrupting!
    cp original.docx test.docx
    python3 corrupt_docx.py test.docx
""")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        sys.exit(1)

    corruption_type = sys.argv[2] if len(sys.argv) > 2 else 'zip_header'

    # Confirm before corrupting
    print(f"About to corrupt: {filename}")
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)

    corrupt_docx_file(filename, corruption_type)
