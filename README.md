# higher

This project includes a small webpage for practising past paper questions.

## Extracting questions

Install the Python dependency `PyMuPDF` which is used to convert PDF pages
directly to images:

```bash
pip install PyMuPDF
```

Run `generate_index.py` to process the provided PDF. The script skips the
multiple choice sections (page ranges are configured inside the script) and pairs
each remaining page with the following page as its answer. All images are
embedded directly in `data.js` so the site works offline:

```bash
python3 generate_index.py
```

`index.html` loads the resulting `data.js`, so no external images are required.

Once `data.js` is generated, simply open `index.html` in your browser (or run
`python3 -m http.server` and browse to `http://localhost:8000`) to view random
questions and reveal their answers.

