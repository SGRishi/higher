import json
import subprocess
import re
from pathlib import Path
import base64
import argparse

PDF = "Higher-Past-Papers by topic.pdf"
OUTDIR = "pages"

# Page ranges to skip (inclusive) - multiple choice sections
SKIP_RANGES = [
    (242, 260),
    (380, 398),
    (448, 470),
]

# Determine page count
parser = argparse.ArgumentParser(description="Generate data.js with embedded questions and answers")
parser.add_argument("--max-pages", type=int, default=0,
                    help="limit number of pages to process (for testing)")
args = parser.parse_args()

info = subprocess.check_output(['pdfinfo', PDF]).decode('utf-8')
match = re.search(r'Pages:\s+(\d+)', info)
num_pages = int(match.group(1)) if match else 0
if args.max_pages and args.max_pages < num_pages:
    num_pages = args.max_pages

pairs = []
page = 1

def ensure_png(page_num):
    path = Path(OUTDIR) / f"page-{page_num:03d}.png"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "pdftoppm",
            "-png",
            "-f",
            str(page_num),
            "-l",
            str(page_num),
            PDF,
            str(path.with_suffix(""))
        ], check=True)
    return path

def to_data_uri(path: Path) -> str:
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{encoded}"

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
    q_path = ensure_png(q)
    a_path = ensure_png(a)
    pairs.append({
        'question': to_data_uri(q_path),
        'answer': to_data_uri(a_path)
    })
    page += 1

with open('data.js', 'w') as f:
    f.write('const data = ')
    json.dump(pairs, f)
    f.write(';')
