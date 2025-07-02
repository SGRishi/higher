# higher

This project includes a small webpage for practising past paper questions.

## Extracting questions

To convert pages from the included PDF into individual PNG images, install
`poppler-utils` and run the helper script:

```bash
sudo apt-get install poppler-utils
./extract_pages.sh -f 1 -l 1  # extract page 1 only
```

The script uses `pdftoppm` to generate PNG images in the `pages/` folder.
Pass `-f` and `-l` to choose which pages to extract.
