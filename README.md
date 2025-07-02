# higher

This project includes a small webpage for practising past paper questions.

## Extracting questions

To convert pages from the included PDF into individual PNG images, first install
`poppler-utils` and run the helper script:

```bash
sudo apt-get install -y poppler-utils pdfgrep
./extract_pages.sh -f 1 -l 525  # extract all pages
```

`extract_pages.sh` uses `pdftoppm` to generate PNG images in the `pages/`
folder. After generating the PNGs, create `index.json` describing the question
and answer pairs:

```bash
python3 generate_index.py
```

The script skips the multiple choice sections and pairs each remaining page
with the next page as its answer. Open `index.html` in a browser to view random
questions.

