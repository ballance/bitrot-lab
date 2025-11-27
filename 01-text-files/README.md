# Text Files - The Basics

## What is a Text File?

A text file is just a sequence of bytes that represent characters. There are different ways to encode characters as bytes:

### ASCII (American Standard Code for Information Interchange)
- Uses **7 bits** (values 0-127)
- Only supports basic English characters
- Example: 'A' = 65, 'a' = 97, '0' = 48

### UTF-8 (Unicode)
- **Backwards compatible** with ASCII for basic characters
- Can represent **any character** in any language using 1-4 bytes
- Example: 'A' = 65 (1 byte), '😀' = 0xF0 0x9F 0x98 0x80 (4 bytes)

## Files in This Directory

- `simple-ascii.txt` - Basic ASCII text
- `utf8-examples.txt` - UTF-8 with emoji and special characters
- `line-endings.txt` - Shows different line ending styles

## Experiments to Try

### 1. View the hex representation
```bash
xxd simple-ascii.txt
xxd utf8-examples.txt
```

**What to notice:**
- ASCII characters appear on the right side
- Each character's hex code on the left
- UTF-8 multi-byte characters look different

### 2. Compare byte counts
```bash
wc -c simple-ascii.txt    # byte count
wc -m simple-ascii.txt    # character count
wc -c utf8-examples.txt   # bytes
wc -m utf8-examples.txt   # characters (notice the difference!)
```

### 3. Corrupt a file
```bash
# Make a copy first!
cp simple-ascii.txt corrupted.txt

# Use Python to flip some bits
python3 ../tools/corrupt_text.py corrupted.txt

# Try to read it
cat corrupted.txt

# View in hex to see what changed
xxd corrupted.txt
```

## Questions to Explore

1. What happens if you change one byte in the middle of a UTF-8 emoji?
2. Can you find the byte values for newline characters? (Hint: 0x0A)
3. What happens if you delete the first byte of a UTF-8 file?
4. Can you create a file that looks normal in a text editor but has hidden characters?

## Line Endings

Different operating systems use different bytes for "new line":
- **Unix/Mac (LF)**: `0x0A`
- **Windows (CRLF)**: `0x0D 0x0A`
- **Old Mac (CR)**: `0x0D`

You can see these in the hex view!
