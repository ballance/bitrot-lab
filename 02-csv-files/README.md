# CSV Files - Structured Text Data

## What is CSV?

CSV stands for "Comma-Separated Values". It's a simple way to store tabular data (like a spreadsheet) in a text file.

**Structure:**
```
name,age,city
Alice,25,New York
Bob,30,Seattle
```

## Important Rules

1. **Commas** separate columns (fields)
2. **Newlines** separate rows (records)
3. **Quotes** protect commas inside data: `"Smith, John",42,Boston`
4. **First row** is often column headers

## Files in This Directory

- `students.csv` - Simple student data
- `products.csv` - Product catalog with prices
- `messy.csv` - CSV with quotes, commas in data

## Experiments to Try

### 1. View as text vs hex
```bash
cat students.csv
xxd students.csv
```

**Notice:** It's just text! Commas are 0x2C, newlines are 0x0A

### 2. What breaks a CSV?

Try corrupting with Python:
```bash
cp students.csv broken.csv
python3 ../tools/corrupt_csv.py broken.csv
```

**Corruption scenarios:**
- Remove a comma → column misalignment
- Remove a quote → parsing fails
- Change delimiter → data looks wrong
- Remove a newline → two rows merge

### 3. Open in spreadsheet software
```bash
# On Mac
open students.csv
```

Then open the corrupted version - see what happens!

### 4. Parse with Python
```bash
python3 -c "
import csv
with open('students.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
"
```

## Questions to Explore

1. What happens if you remove one comma from the middle of a row?
2. Can you create a CSV that looks normal in a text editor but crashes Excel?
3. What if there's data with a comma inside it but no quotes?
4. What happens if you change a comma to a semicolon? (Some countries use ; instead!)

## CSV Variations

Different programs might expect:
- **Delimiter**: comma, semicolon, tab, pipe
- **Quote character**: double quote " or single quote '
- **Escape character**: backslash \ or double-quote ""
- **Line ending**: LF or CRLF

These variations can cause compatibility issues!
