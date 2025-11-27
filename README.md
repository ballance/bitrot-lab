# File Format & Corruption Learning Lab

**A hands-on exploration of how files really work**

## What You'll Learn

By the end of this lab, you'll understand:

1. **Files are just bytes** - Every file is a sequence of numbers (0-255)
2. **Different formats, different rules** - How text, CSV, DOCX, and images store data
3. **Magic numbers matter** - File signatures that identify formats
4. **Corruption reveals structure** - Breaking files teaches you how they work
5. **Hex editors are X-ray vision** - See the raw data behind any file

## Prerequisites

**Skills needed:**
- Basic command line (cd, ls, cat)
- Python basics (we provide all scripts, but you should understand them)
- Text editor usage

**Tools needed (already on your Mac):**
- `xxd` - hex viewer
- `hexdump` - alternative hex viewer
- `python3` - for corruption scripts
- `unzip` - for exploring DOCX files

## Project Structure

```
bitrot-lab/
├── 01-text-files/          # Start here! ASCII & UTF-8 basics
│   ├── README.md           # Learn about character encoding
│   └── *.txt               # Example files to explore
│
├── 02-csv-files/           # Structured data as text
│   ├── README.md           # CSV format deep dive
│   └── *.csv               # Data files to corrupt and fix
│
├── 03-docx-files/          # The "secret" ZIP format
│   ├── README.md           # Unzip Word docs!
│   └── *.docx              # Documents to dissect
│
├── 04-binary-files/        # Images and magic numbers
│   ├── README.md           # PNG structure explained
│   └── *.png, *.bmp        # Binary files to examine
│
├── tools/                  # Corruption utilities
│   ├── corrupt_text.py     # Break text files safely
│   ├── corrupt_csv.py      # CSV corruption experiments
│   ├── corrupt_docx.py     # DOCX structure breaker
│   ├── corrupt_binary.py   # Image glitching tool
│   └── analyze_png.py      # PNG chunk analyzer
│
└── hex-editor-guide.md     # Complete xxd tutorial
```

## Quick Start

**First time? Start here:**

```bash
# 1. Read the hex editor guide first
cat hex-editor-guide.md

# 2. Try viewing a simple file
xxd 01-text-files/simple-ascii.txt

# 3. Follow the learning path below
```

## Recommended Learning Path

### Phase 1: Text Files (30-45 minutes)
**Goal:** Understand that characters are just numbers

1. Read `01-text-files/README.md`
2. View files with `xxd` to see character encodings
3. Compare ASCII vs UTF-8 byte counts
4. Corrupt a file and see what breaks
5. **Key insight:** Text files are bytes that happen to map to characters

### Phase 2: CSV Files (30 minutes)
**Goal:** Learn how structure emerges from simple rules

1. Read `02-csv-files/README.md`
2. View CSV files as hex - they're just text!
3. Remove one comma, see columns misalign
4. Try parsing corrupted CSV with Python
5. **Key insight:** Simple delimiters create complex data structures

### Phase 3: DOCX Files (45-60 minutes)
**Goal:** Discover compound file formats

1. Read `03-docx-files/README.md`
2. Check the magic number: `xxd -l 16 *.docx`
3. Unzip a DOCX file - it's XML inside!
4. Edit `word/document.xml` directly
5. Re-zip and open in Word
6. **Key insight:** Modern formats are often archives of structured data

### Phase 4: Binary Files (45-60 minutes)
**Goal:** Understand non-text formats and magic numbers

1. Read `04-binary-files/README.md`
2. Identify PNG signature: `89 50 4E 47`
3. Use `analyze_png.py` to see chunk structure
4. Corrupt the header vs image data - see different failures
5. Compare corrupted regions with `xxd`
6. **Key insight:** Binary formats use every byte efficiently

## Tools Reference

### Hex Viewing
```bash
# Basic hex view
xxd filename

# First 64 bytes only
xxd -l 64 filename

# Compare two files
diff <(xxd file1) <(xxd file2)
```

### File Corruption (Safe!)
```bash
# Text file corruption
python3 tools/corrupt_text.py file.txt

# CSV corruption with specific type
python3 tools/corrupt_csv.py file.csv

# DOCX corruption
python3 tools/corrupt_docx.py file.docx

# Binary corruption (header or data)
python3 tools/corrupt_binary.py file.png --corrupt-header
python3 tools/corrupt_binary.py file.png --glitch
```

### Analysis Tools
```bash
# Analyze PNG structure
python3 tools/analyze_png.py image.png

# Unzip DOCX to explore
unzip document.docx -d extracted/
```

## Core Concepts

### Magic Numbers (File Signatures)
The first few bytes identify the file type:
- PNG: `89 50 4E 47` (.PNG)
- ZIP/DOCX: `50 4B 03 04` (PK..)
- JPEG: `FF D8 FF`
- GIF: `47 49 46 38` (GIF8)
- PDF: `25 50 44 46` (%PDF)

**Try it:** `xxd -l 16 <any-file>` and identify the format!

### Character Encoding
- **ASCII:** 1 byte per character (English only)
- **UTF-8:** 1-4 bytes per character (all languages + emoji)
- Example: 'A' = `0x41`, '😀' = `0xF0 0x9F 0x98 0x80`

### File Corruption Types
1. **Header corruption** - File won't open at all
2. **Structure corruption** - Parser fails (XML, CSV)
3. **Data corruption** - Content is wrong but file opens
4. **Truncation** - File ends too early
5. **Extension mismatch** - File is valid but OS confused

## Experiments to Try

### Easy
- [ ] Find the magic number of 5 different file types
- [ ] Change one letter in a text file using only hex editing
- [ ] Count newlines (0x0A) in a text file
- [ ] Make a CSV that Excel can't parse

### Medium
- [ ] Unzip a DOCX, edit the text in XML, re-zip, and open
- [ ] Create a valid 2x2 BMP image by hand in hex
- [ ] Corrupt a PNG header vs data - compare the failures
- [ ] Find all UTF-8 multi-byte characters in a file

### Advanced
- [ ] Create a polyglot file (valid as both PNG and ZIP)
- [ ] Write a Python script to extract images from DOCX
- [ ] Recover a "deleted" file by finding its magic number
- [ ] Create a minimal valid PNG from scratch in hex

## Learning Outcomes

After completing this lab, you'll be able to:

- **Read hex dumps** and understand what you're seeing
- **Identify file formats** from magic numbers alone
- **Debug file corruption** by examining raw bytes
- **Understand character encoding** (ASCII vs UTF-8)
- **Explain compound formats** like DOCX (ZIP + XML)
- **Programmatically manipulate** file structures
- **Reverse engineer** simple binary formats

## Why This Matters

Understanding files at the byte level helps you:

- **Debug weird bugs** - "Why won't this CSV import?"
- **Recover data** - Find file signatures in corrupted drives
- **Validate uploads** - Check actual format, not just extension
- **Optimize storage** - Understand compression and efficiency
- **Build better software** - Know how libraries parse files
- **Security awareness** - Detect file type spoofing

## Safety and Ethics

**This lab teaches you:**
- How to examine file structures
- How corruption happens
- How to repair simple corruption

**Do NOT use this knowledge to:**
- Corrupt files you don't own
- Bypass security measures
- Hide malicious files in other formats
- Damage systems or data

**All experiments are in this isolated directory. Always work on copies!**

## Tips for Success

1. **Read the guides first** - Each README has important concepts
2. **Start small** - Use tiny files to see patterns clearly
3. **Make copies** - Never corrupt original files
4. **Take notes** - Document what you learn
5. **Compare working vs broken** - Use `diff <(xxd file1) <(xxd file2)`
6. **Ask "why?"** - Every byte has a purpose
7. **Experiment freely** - You can't break anything here!

## Next Steps

After completing this lab:

1. **Explore other formats:** PDF, MP3, SQLite databases
2. **Learn file recovery:** Tools like `foremost`, `photorec`
3. **Study compression:** How ZIP, PNG, JPEG compress data
4. **Investigate cryptography:** How encryption transforms bytes
5. **Build a parser:** Write code to read a binary format

## Getting Help

**Stuck? Try this:**
1. Re-read the README for that section
2. Check `hex-editor-guide.md` for xxd usage
3. Compare your hex dump with a working file
4. Look at the Python scripts - they show how to manipulate bytes

**Questions to explore:**
- "What happens if I change this byte?"
- "Can I find where this data is stored?"
- "Why does this format need this header?"
- "What's the minimal valid version of this file?"

## Q&A - Common Questions

### General Questions

**Q: Do I need to be an experienced programmer to use this lab?**
A: No! If you know basic command line and can read Python, you're ready. The lab is designed to teach you about file formats from the ground up.

**Q: Will this lab help me with my day-to-day programming?**
A: Absolutely. Understanding how files work at the byte level helps you debug mysterious file parsing errors, validate file uploads properly, understand why compression works, and generally demystifies how data is stored.

**Q: How long does it take to complete?**
A: The core learning path takes 2-3 hours if you follow all four phases. But you can go at your own pace and revisit sections as needed.

**Q: Can I skip ahead to the binary files section?**
A: You can, but it's better to go in order. Each section builds on concepts from the previous one, and starting with text files gives you essential foundations.

### Technical Questions

**Q: What if I accidentally corrupt an important file?**
A: All experiments should be done in this directory only, and always work on copies. The corruption scripts are designed for learning, not for use on real files.

**Q: Why do some files show weird characters in the hex editor?**
A: Non-printable bytes (like 0x00-0x1F and 0x80-0xFF) often display as dots or special symbols. That's normal - they're just bytes that don't map to visible characters.

**Q: I broke a file and can't figure out what's wrong. What do I do?**
A: Use `diff <(xxd original.txt) <(xxd corrupted.txt)` to compare the hex dumps. This shows exactly which bytes changed. Understanding the difference is often the best learning experience!

**Q: Can I use a GUI hex editor instead of `xxd`?**
A: Yes! Tools like Hex Fiend or ImHex are great, especially for larger files. But learning `xxd` first is valuable because it's always available on any Unix-like system.

**Q: What's the difference between a text file and a binary file?**
A: It's just convention. ALL files are binary (sequences of bytes). "Text files" are files where those bytes happen to represent readable characters using encodings like ASCII or UTF-8.

### Learning Path Questions

**Q: I finished all four phases. What should I learn next?**
A: Great question! Consider exploring:
- Other file formats like PDF, MP3, or video formats
- File carving and data recovery techniques
- How compression algorithms work (ZIP, GZIP)
- Binary protocol analysis (network packets)
- Writing your own simple file format parser

**Q: The Python scripts are interesting. Can I modify them?**
A: Absolutely! Modifying the scripts to do different types of corruption or analysis is an excellent way to deepen your understanding.

**Q: Are there similar resources for learning about networking or databases?**
A: That's outside the scope of this lab, but the same principles apply. Network packets and database files are also just bytes with specific structures.

### Questions or Feedback?

**Have a question not answered here? Found something confusing? Want to share what you learned?**

Please reach out! You can:
- Open an issue on GitHub with your question
- Share your experiments and what you discovered
- Suggest improvements to make this lab better for other learners
- Ask for clarification on any concept

Learning about low-level file formats can feel abstract at first, but hands-on exploration makes it click. Don't hesitate to ask questions - that's how we all learn!

---

**Ready to see what files really are? Start with `01-text-files/`**
