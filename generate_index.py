import json
import subprocess
import re
from pathlib import Path

PDF = "Higher-Past-Papers by topic.pdf"
OUTDIR = "pages"

# Page ranges to skip (inclusive) - multiple choice sections
SKIP_RANGES = [
    (242, 260),
    (380, 398),
    (448, 470),
]

# Determine page count
info = subprocess.check_output(['pdfinfo', PDF]).decode('utf-8')
match = re.search(r'Pages:\s+(\d+)', info)
num_pages = int(match.group(1)) if match else 0

pairs = []
page = 1

def in_skip(p):
    for s,e in SKIP_RANGES:
        if s <= p <= e:
            return True
    return False

while page < num_pages:
    if in_skip(page):
        page += 1
        continue
    q = page
    page += 1
    while page <= num_pages and in_skip(page):
        page += 1
    if page > num_pages:
        break
    a = page
    pairs.append({
        'question': f'{OUTDIR}/page-{q:03d}.png',
        'answer': f'{OUTDIR}/page-{a:03d}.png'
    })
    page += 1

with open('index.json', 'w') as f:
    json.dump(pairs, f, indent=2)
