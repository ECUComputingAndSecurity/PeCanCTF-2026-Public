#!/usr/bin/env python3
"""Solve script for Dictionary Site CTF challenge.

Visits every word page via sitemap.xml and searches for the flag (pecan{...}).
Usage:
    python3 solve.py [base_url]
    Default base_url: http://localhost:3000
"""
import sys
import re
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"

def fetch(path):
    req = Request(f"{BASE}{path}", headers={"User-Agent": "solve.py"})
    with urlopen(req) as r:
        return r.read().decode()

sitemap = fetch("/sitemap.xml")
root = ET.fromstring(sitemap)
ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [loc.text for loc in root.findall(".//ns:loc", ns)]

print(f"[*] Found {len(urls)} URLs in sitemap")

for i, url in enumerate(urls, 1):
    html = fetch(url)
    match = re.search(r"pecan\{[^}]+\}", html, re.IGNORECASE)
    if match:
        print(f"[+] FLAG FOUND on page {url}: {match.group(0)}")
        break
    if i % 100 == 0:
        print(f"[*] Checked {i}/{len(urls)}...")
else:
    print("[-] Flag not found")
