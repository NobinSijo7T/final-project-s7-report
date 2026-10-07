import sys
import glob
import json
import os
import re

files = sorted(glob.glob('references/extracted/*.json'))

papers = []

for idx, fpath in enumerate(files):
    fname = os.path.basename(fpath)
    d = json.load(open(fpath, encoding='utf-8'))
    txt = d.get('full_text', '')
    
    # Let's inspect the first 2500 characters
    header_chunk = txt[:3500]
    
    # DOI search
    doi_match = re.search(r'(?:https?://doi\.org/|doi:\s*)(10\.[0-9]{4,9}/[^\s,]+)', header_chunk)
    doi = doi_match.group(1).rstrip('.') if doi_match else ''
    
    # Split non-empty lines
    lines = [l.strip() for l in header_chunk.split('\n') if l.strip()]
    
    papers.append({
        'id': idx + 1,
        'filename': fname,
        'doi': doi,
        'lines': lines[:20]
    })

with open('references/all_extracted_details.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=2, ensure_ascii=False)

print(f"Dumped details for {len(papers)} papers.")
