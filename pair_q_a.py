import fitz

pdf = 'Higher-Past-Papers by topic.pdf'
doc = fitz.open(pdf)
current_pages = []
output = []

for i, page in enumerate(doc, start=1):
    text = page.get_text()
    lower = text.lower()
    if 'additional guidance' in lower:
        if current_pages:
            question_text = "\n".join(doc[j-1].get_text() for j in current_pages)
            output.append({
                'question_pages': current_pages.copy(),
                'answer_page': i,
                'question_text': question_text,
                'answer_text': text
            })
            current_pages = []
    else:
        current_pages.append(i)

with open('pairs.txt', 'w') as f:
    for idx, pair in enumerate(output, 1):
        f.write(f"Pair {idx}: Question pages {pair['question_pages']} -> Answer page {pair['answer_page']}\n")
        f.write(pair['question_text'].strip().replace('\n',' ')[:200] + "\n")
        f.write('Answer snippet: ' + pair['answer_text'].strip().replace('\n',' ')[:200] + "\n---\n")
print('Total pairs', len(output))
