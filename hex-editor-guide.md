# Hex Editor Guide for Beginners

## What is a Hex Editor?

A hex editor lets you see and edit the **raw bytes** of any file. Instead of seeing text or images, you see the actual numbers stored on disk.

## Why Use Hexadecimal?

**Hexadecimal (hex)** is base-16 numbering:
- Uses digits: 0-9 and letters: A-F
- One hex digit = 4 bits
- Two hex digits = 1 byte (8 bits)

Examples:
- `0x00` = 0 in decimal
- `0x0A` = 10 in decimal (newline character)
- `0xFF` = 255 in decimal
- `0x41` = 65 in decimal (letter 'A')

## Using xxd (Your Main Tool)

### Basic Usage

View a file:
```bash
xxd filename.txt
```

Output format:
```
00000000: 4865 6c6c 6f2c 2057 6f72 6c64 210a       Hello, World!.
│         │                                        │
│         └─ Hex bytes (2 digits per byte)        └─ ASCII representation
└─ Offset (position in file)
```

### Useful xxd Options

View first 64 bytes:
```bash
xxd -l 64 filename
```

View specific range (skip 100 bytes, show 50):
```bash
xxd -s 100 -l 50 filename
```

Group bytes differently (4 bytes per group):
```bash
xxd -g 4 filename
```

Show only hex (no ASCII):
```bash
xxd -p filename
```

Reverse hex dump back to binary:
```bash
xxd -r hexdump.txt output.bin
```

### Edit Files with xxd

This is a two-step process:

1. Create hex dump:
```bash
xxd file.txt > file.hex
```

2. Edit `file.hex` in a text editor

3. Convert back to binary:
```bash
xxd -r file.hex file.txt
```

**Be careful!** This directly modifies bytes.

## Using hexdump

Alternative hex viewer with different formats:

Canonical format (similar to xxd):
```bash
hexdump -C filename
```

Show as decimal instead of hex:
```bash
hexdump -d filename
```

Custom format (one byte per line):
```bash
hexdump -e '1/1 "%02X\n"' filename
```

## Reading Hex Dumps

### Example: "Hello"

```
00000000: 4865 6c6c 6f0a                           Hello.
```

Breaking it down:
- `48` = 'H' (72 in decimal)
- `65` = 'e' (101 in decimal)
- `6c` = 'l' (108 in decimal)
- `6c` = 'l' (108 in decimal)
- `6f` = 'o' (111 in decimal)
- `0a` = newline (10 in decimal)

### Example: PNG signature

```
00000000: 8950 4e47 0d0a 1a0a                      .PNG....
```

- `89` = Non-ASCII (prevents text display)
- `50 4E 47` = "PNG"
- `0D 0A` = Windows line ending (CRLF)
- `1A` = DOS end-of-file character
- `0A` = Unix line ending (LF)

This signature helps detect file corruption during transmission!

## Common Byte Values to Know

| Hex  | Decimal | ASCII | Meaning |
|------|---------|-------|---------|
| 0x00 | 0       | NUL   | Null byte (string terminator in C) |
| 0x09 | 9       | TAB   | Tab character |
| 0x0A | 10      | LF    | Line Feed (Unix newline) |
| 0x0D | 13      | CR    | Carriage Return |
| 0x20 | 32      | SPACE | Space character |
| 0x30-0x39 | 48-57 | 0-9 | Digits |
| 0x41-0x5A | 65-90 | A-Z | Uppercase letters |
| 0x61-0x7A | 97-122 | a-z | Lowercase letters |
| 0xFF | 255     | ÿ     | Maximum byte value |

## Hands-On Exercises

### Exercise 1: Find the Magic Number
```bash
xxd -l 16 04-binary-files/example.png
xxd -l 16 03-docx-files/example.docx
xxd -l 16 01-text-files/simple-ascii.txt
```

**Question:** Which files have special signatures?

### Exercise 2: Count Newlines
```bash
xxd 01-text-files/simple-ascii.txt | grep "0a"
```

**Question:** How many newlines (0x0A) can you find?

### Exercise 3: Find a Word
```bash
xxd 01-text-files/simple-ascii.txt | grep "Hello"
```

Look at the hex values for each letter!

### Exercise 4: Edit a Byte

1. Create test file:
```bash
echo "ABCDE" > test.txt
xxd test.txt
```

2. Dump to hex:
```bash
xxd test.txt > test.hex
cat test.hex
```

3. Edit test.hex - change 42 (B) to 5A (Z)

4. Convert back:
```bash
xxd -r test.hex test.txt
cat test.txt
```

You should see "AZCDE"!

### Exercise 5: Compare Corrupted vs Original
```bash
# Create copies
cp 01-text-files/simple-ascii.txt original.txt
cp 01-text-files/simple-ascii.txt corrupted.txt

# Corrupt one
python3 tools/corrupt_text.py corrupted.txt random

# Compare in hex
diff <(xxd original.txt) <(xxd corrupted.txt)
```

The diff shows exactly which bytes changed!

## Advanced: Creating Files from Hex

You can create any file by writing hex!

Create a tiny text file:
```bash
echo "48 65 6c 6c 6f 0a" | xxd -r -p > hello.txt
cat hello.txt  # Shows "Hello"
```

Create a 1x1 pixel BMP (tiny!):
```bash
# This creates a minimal BMP - try it!
# (Exercise: research BMP format and create this)
```

## Tips for Exploring

1. **Always work on copies** - never corrupt original files
2. **Start small** - use tiny files to understand patterns
3. **Compare** - look at hex of working vs broken files
4. **Document** - write down what you learn
5. **Experiment** - try changing one byte and see what happens

## Practice Challenge

Can you:
1. Create a text file
2. Convert it to hex
3. Manually edit the hex to change the text
4. Convert back to a file
5. Verify the text changed

This teaches you that files are just bytes, and you have full control!

## Going Further

Other hex editors to explore later:
- **hexyl** - colorful hex viewer (install with: `brew install hexyl`)
- **Hex Fiend** - GUI hex editor for Mac (install with: `brew install --cask hex-fiend`)
- **ImHex** - Pattern-based hex editor

But xxd is perfect for learning - it's simple and powerful!
