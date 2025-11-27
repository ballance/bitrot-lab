# DOCX Files - Zipped XML!

## The Big Secret About .docx Files

**A .docx file is actually a ZIP archive containing XML files!**

This is true for all Microsoft Office files since 2007:
- `.docx` - Word documents
- `.xlsx` - Excel spreadsheets
- `.pptx` - PowerPoint presentations

## Proof: Unzip a DOCX!

```bash
# Make a copy
cp example.docx example.zip

# Unzip it
unzip example.zip -d extracted/

# Look inside
ls -la extracted/
cat extracted/word/document.xml
```

## Structure of a DOCX

```
example.docx (ZIP file)
├── [Content_Types].xml      # File type definitions
├── _rels/                    # Relationships between files
├── word/
│   ├── document.xml         # MAIN CONTENT HERE!
│   ├── styles.xml           # Text styles
│   ├── settings.xml         # Document settings
│   ├── _rels/               # Relationships
│   └── media/               # Images, etc.
└── docProps/                # Document properties (author, etc.)
```

## Files in This Directory

- `example.docx` - Simple Word document
- `with-images.docx` - Contains an embedded image
- `extracted/` - Unzipped contents (run the commands to create)

## Experiments to Try

### 1. View as hex - see the ZIP signature
```bash
xxd -l 32 example.docx
```

**Look for:** `50 4B 03 04` at the start - that's the ZIP "magic number"!

### 2. Unzip and explore
```bash
mkdir -p extracted
unzip example.docx -d extracted
tree extracted/   # or: ls -R extracted/
```

### 3. Edit the XML directly
```bash
# Extract
unzip example.docx -d edit_me

# Edit the content (use any text editor)
# On Mac:
open -a TextEdit edit_me/word/document.xml

# Re-zip it
cd edit_me
zip -r ../modified.docx *
cd ..

# Open in Word
open modified.docx
```

### 4. Break it in interesting ways
```bash
python3 ../tools/corrupt_docx.py example.docx
```

**Corruption scenarios:**
- Delete the ZIP header → won't open at all
- Corrupt document.xml → Word can't parse content
- Remove a file → Word tries to repair
- Break the relationships → references break

## Questions to Explore

1. What happens if you delete just one byte from the ZIP header?
2. Can you edit text in document.xml and see it change in Word?
3. What if you remove the `_rels` folder?
4. Can you add an image by copying it to `word/media/` and updating the XML?

## Why This Matters

Understanding DOCX structure helps you:
- Recover corrupted documents
- Programmatically create/edit documents
- Understand why files sometimes become "corrupted"
- Debug issues with automated document generation

## XML Inside

The `document.xml` file uses WordprocessingML markup:
```xml
<w:p>  <!-- paragraph -->
  <w:r>  <!-- run (text with same formatting) -->
    <w:t>Hello, World!</w:t>  <!-- text -->
  </w:r>
</w:p>
```

Pretty readable once you know what to look for!
