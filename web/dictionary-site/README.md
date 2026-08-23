# Dictionary Site

## Flag

- `pecan{als0_n0t4_w0rd}`

## Writeup

1. Visit the dictionary site. The homepage has an HTML comment hinting that some non-word entries (flag data) accidentally got mixed into the "Also See" sections during import.
2. Browse the sitemap at `/sitemap.xml` — it lists all 5000+ word pages.
3. Check word pages until you find one with the flag in its "Also See" list.
4. The flag is seeded into the "Also See" list of roughly 50 of the 5000 pages (about 1%), so a sequential crawl typically hits one within the first few hundred requests. The first 500, last 500 and middle 500 entries are deliberately excluded.

### Brute-force approach

- Use the sitemap at `/sitemap.xml` to get all word paths.
- Script through them or manually browse until you spot the non-word entry.
- Example in [solve.py](solve.py) shows how to automate this.

### Notes

- The flag is case-insensitive.
