#!/usr/bin/env python3
"""Diagnostic: why is Saiha's rain forecast missing? Shows how the Aizawl forecast PDF reads.

Run:  python check_pdf_text.py          (needs pypdf, pdfplumber, requests, as for DIWIS)
Prints every line mentioning Saiha/Siaha as read by pypdf and by pdfplumber, plus page rotation.
"""
import io
import re
import requests
import pdfplumber
from pypdf import PdfReader

URL = "https://mausam.imd.gov.in/aizawl/mcdata/AP_forecast.pdf"
HITS = re.compile(r"sai?ha|siaha", re.I)

data = requests.get(URL, headers={"User-Agent": "DIWIS-diagnostic"}, timeout=40).content
print(f"Downloaded {len(data)} bytes from {URL}\n")

reader = PdfReader(io.BytesIO(data))
print("pypdf pages:", len(reader.pages), "| rotation per page:", [p.get("/Rotate", 0) for p in reader.pages])
for number, page in enumerate(reader.pages, 1):
    for line in (page.extract_text() or "").splitlines():
        if HITS.search(line):
            print(f"  pypdf      p{number}: {line.strip()}")

with pdfplumber.open(io.BytesIO(data)) as pdf:
    for number, page in enumerate(pdf.pages, 1):
        for line in (page.extract_text() or "").splitlines():
            if HITS.search(line):
                print(f"  pdfplumber p{number}: {line.strip()}")
        words = page.extract_words()
        print(f"  page {number}: {len(words)} words, {sum(1 for w in words if not w.get('upright', True))} not upright")
