#!/bin/bash
set -e
PDF="Higher-Past-Papers by topic.pdf"
OUTDIR="pages"
mkdir -p "$OUTDIR"
pdftoppm "$PDF" "$OUTDIR/page" -png "$@"
