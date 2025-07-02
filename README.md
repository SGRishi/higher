# higher

This project includes a small webpage for practising past paper questions.

The repository ships with a small sample `data.js` so the page works out of the box. To include every page from the PDF you must generate your own `data.js` as described below.

## Extracting questions

To convert pages from the included PDF into individual PNG images, first install
`poppler-utils` and run the helper script:

```bash
sudo apt-get install -y poppler-utils pdfgrep
./extract_pages.sh -f 1 -l 525  # extract all pages
```

`extract_pages.sh` uses `pdftoppm` to generate PNG images in the `pages/`
folder. After generating the PNGs, run `generate_index.py` to embed the
questions and answers directly in `data.js` as base64 strings:

```bash
python3 generate_index.py
```

The script skips the multiple choice sections and pairs each remaining page
with the next page as its answer. The resulting `data.js` is loaded by
`index.html`, so the site works offline without fetching external images.

Once `data.js` is generated, simply open `index.html` in your browser (or run
`python3 -m http.server` and browse to `http://localhost:8000`) to view random
questions and reveal their answers.

