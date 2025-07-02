import fitz

PDF = 'Higher-Past-Papers by topic.pdf'

doc = fitz.open(PDF)

pairs = []
q_pages = []
started = False
for i, page in enumerate(doc, start=1):
    text = page.get_text()
    lower = text.lower()

    if not started:
        if 'section 2' in lower and 'marks' in lower:
            started = True
        else:
            continue

    if any(kw in lower for kw in (
        'for official use', 'candidate', 'instructions for the completion',
        'data sheet', 'marking instructions')):
        continue

    if 'additional guidance' in lower:
        if q_pages:
            pairs.append((q_pages.copy(), i))
            q_pages = []
    else:
        q_pages.append(i)

# Keep doc open for snippet extraction
with open('pairs.txt', 'w') as f:
    for idx, (q, a) in enumerate(pairs, 1):
        f.write(f"Pair {idx}: Question pages {q} -> Answer page {a}\n")
        qt = ' '.join(doc.load_page(j-1).get_text().replace('\n',' ')[:80] for j in q)
        at = doc.load_page(a-1).get_text().replace('\n',' ')[:80]
        f.write(qt + '\n')
        f.write('Answer snippet: ' + at + '\n---\n')
print('Total pairs', len(pairs))
