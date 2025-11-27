# Binary Files - Images and More

## What Makes a File "Binary"?

**Binary files** contain data that isn't meant to be read as text. They use every possible byte value (0-255) to store information efficiently.

Examples:
- Images: PNG, JPG, GIF
- Audio: MP3, WAV
- Video: MP4, AVI
- Executables: .exe, .app
- Databases: .db, .sqlite

## Magic Numbers (File Signatures)

Most binary files start with a **magic number** - specific bytes that identify the file type:

| Format | Magic Number (Hex) | ASCII |
|--------|-------------------|-------|
| PNG    | `89 50 4E 47`     | `.PNG` |
| JPEG   | `FF D8 FF`        | `...` |
| GIF    | `47 49 46 38`     | `GIF8` |
| ZIP    | `50 4B 03 04`     | `PK..` |
| PDF    | `25 50 44 46`     | `%PDF` |

## Files in This Directory

- `example.png` - Small PNG image (created programmatically)
- `simple.bmp` - Simple bitmap (easier to understand than PNG)
- File format reference charts

## Experiments to Try

### 1. Check the magic number
```bash
xxd -l 16 example.png
# Look for: 89 50 4E 47 at the start
```

### 2. Break the magic number
```bash
cp example.png broken.png
python3 ../tools/corrupt_binary.py broken.png --corrupt-header
open broken.png  # Won't open! OS doesn't recognize it
```

### 3. View the whole structure
```bash
xxd example.png | less
# Use arrow keys to scroll, 'q' to quit
```

### 4. Corrupt in the middle
```bash
cp example.png glitched.png
python3 ../tools/corrupt_binary.py glitched.png --glitch
open glitched.png  # Might partially display!
```

## PNG Structure

PNG files are organized into **chunks**:

```
PNG Signature: 89 50 4E 47 0D 0A 1A 0A  (8 bytes)

Then chunks:
[Length][Type][Data][CRC]

Critical chunks:
- IHDR: Image header (dimensions, color type)
- PLTE: Palette (for indexed color images)
- IDAT: Image data (compressed)
- IEND: Image end marker

Ancillary chunks:
- tEXt: Text comments
- tIME: Modification time
- etc.
```

### View PNG chunks
```bash
python3 ../tools/analyze_png.py example.png
```

## Questions to Explore

1. What happens if you change byte 0 from `89` to `88`?
2. Can you find where image data vs metadata is stored?
3. What if you delete bytes from the middle?
4. Can you manually create a tiny valid PNG in hex?
5. What happens if you change the file extension but not the content?

## Bitmap (BMP) - Simpler Format

BMP files are **uncompressed**, making them easier to understand:

```
Header (14 bytes):
- Magic: 'BM' (42 4D)
- File size
- Reserved
- Offset to pixel data

DIB Header (40+ bytes):
- Width, Height
- Color planes
- Bits per pixel
- Compression (usually 0 = none)

Pixel Data:
- Raw RGB values
- Padding to 4-byte alignment
- Bottom-to-top by default!
```

Try creating a 2x2 pixel BMP by hand!

## Corruption Effects

Different corruption types cause different effects:

| Corruption | Effect |
|------------|--------|
| Header broken | File won't open at all |
| Magic number wrong | OS doesn't recognize format |
| Metadata corrupted | Displays wrong but might show something |
| Image data corrupted | Glitchy/distorted image |
| File truncated | Partial image |
| Extra data at end | Usually ignored |

## Why This Matters

Understanding binary formats helps with:
- File recovery (find the magic number!)
- Detecting file type regardless of extension
- Understanding compression
- Creating files programmatically
- Debugging file handling code
