#!/usr/bin/env python3
"""
PNG File Analyzer
Displays PNG chunk structure and validates format
"""

import sys
import struct
import zlib

def read_chunk(f):
    """Read a PNG chunk from file"""
    # Length (4 bytes)
    length_data = f.read(4)
    if len(length_data) < 4:
        return None

    length = struct.unpack('>I', length_data)[0]

    # Type (4 bytes)
    chunk_type = f.read(4)
    if len(chunk_type) < 4:
        return None

    # Data
    data = f.read(length)
    if len(data) < length:
        return None

    # CRC (4 bytes)
    crc = struct.unpack('>I', f.read(4))[0]

    # Verify CRC
    calculated_crc = zlib.crc32(chunk_type + data) & 0xffffffff
    crc_valid = (crc == calculated_crc)

    return {
        'type': chunk_type.decode('ascii', errors='replace'),
        'length': length,
        'data': data,
        'crc': crc,
        'crc_valid': crc_valid
    }

def analyze_png(filename):
    """Analyze PNG file structure"""

    print(f"Analyzing: {filename}\n")

    with open(filename, 'rb') as f:
        # Check PNG signature
        signature = f.read(8)
        expected_sig = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

        print("PNG Signature:")
        print(f"  Expected: {expected_sig.hex()}")
        print(f"  Found:    {signature.hex()}")

        if signature == expected_sig:
            print("  ✓ Valid PNG signature\n")
        else:
            print("  ✗ INVALID signature - not a valid PNG!\n")
            return

        # Read chunks
        print("Chunks:")
        print(f"{'Type':<12} {'Length':<10} {'CRC':<6} {'Description'}")
        print("-" * 70)

        chunk_num = 0
        while True:
            chunk = read_chunk(f)
            if chunk is None:
                break

            chunk_num += 1
            crc_status = "✓" if chunk['crc_valid'] else "✗"

            # Describe chunk
            descriptions = {
                'IHDR': 'Image header',
                'PLTE': 'Palette',
                'IDAT': 'Image data',
                'IEND': 'Image end',
                'tRNS': 'Transparency',
                'gAMA': 'Gamma',
                'cHRM': 'Chromaticity',
                'sRGB': 'sRGB color space',
                'iCCP': 'ICC color profile',
                'tEXt': 'Text',
                'zTXt': 'Compressed text',
                'iTXt': 'International text',
                'bKGD': 'Background color',
                'pHYs': 'Physical pixel dimensions',
                'tIME': 'Last modification time',
            }

            desc = descriptions.get(chunk['type'], 'Unknown chunk type')

            print(f"{chunk['type']:<12} {chunk['length']:<10} {crc_status:<6} {desc}")

            # Parse IHDR
            if chunk['type'] == 'IHDR' and len(chunk['data']) >= 13:
                width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack('>IIBBBBB', chunk['data'])

                color_types = {
                    0: "Grayscale",
                    2: "RGB",
                    3: "Palette",
                    4: "Grayscale + Alpha",
                    6: "RGB + Alpha"
                }

                print(f"             Width: {width}, Height: {height}")
                print(f"             Bit depth: {bit_depth}, Color: {color_types.get(color_type, 'Unknown')}")
                print(f"             Compression: {compression}, Filter: {filter_method}, Interlace: {interlace}")

            # Parse tEXt
            elif chunk['type'] == 'tEXt':
                try:
                    text = chunk['data'].decode('latin1')
                    print(f"             Text: {text[:60]}...")
                except:
                    pass

        print("\n" + "=" * 70)
        print(f"Total chunks: {chunk_num}")

def show_help():
    print("""
PNG File Analyzer

Usage:
    python3 analyze_png.py <filename>

This tool displays:
- PNG signature validation
- All chunks in the file
- Chunk types, lengths, and CRC validation
- IHDR (header) details: dimensions, color type, etc.

Example:
    python3 analyze_png.py image.png
""")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        sys.exit(1)

    analyze_png(filename)
