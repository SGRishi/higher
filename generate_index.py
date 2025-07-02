import json
import base64
import argparse
from pathlib import Path
import fitz  # PyMuPDF

PDF = "Higher-Past-Papers by topic.pdf"
OUTDIR = "pages"

# Page ranges to skip (inclusive) - multiple choice sections
# Multiple choice sections in the PDF
# These were determined manually by inspecting the document.
# Each tuple is inclusive start and end page numbers.
SKIP_RANGES = [
    (242, 304),  # Specimen multi choice
    (310, 347),  # Past paper multi choice
    (380, 409),  # Past paper multi choice
    (448, 479),  # Past paper multi choice
]

# Determine page count
parser = argparse.ArgumentParser(
    description="Generate data.js with embedded questions and answers"
)
parser.add_argument(
    "--max-pages", type=int, default=0,
    help="limit number of pages to process (for testing)"
)
args = parser.parse_args()

doc = fitz.open(PDF)
num_pages = len(doc)
if args.max_pages and args.max_pages < num_pages:
    num_pages = args.max_pages

pairs = []
page = 1

def ensure_png(page_num):
    path = Path(OUTDIR) / f"page-{page_num:03d}.png"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        page = doc.load_page(page_num - 1)
        pix = page.get_pixmap(dpi=150)
        pix.save(path)
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

while page <= num_pages:
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

doc.close()
