import json
import re

files = [
    's11036-025-02465-6.json',
    's11047-025-10023-y.json',
    's13677-025-00828-8.json',
    's00521-023-09033-7.json',
    's00521-024-10620-5.json',
    's13428-023-02062-z.json'
]

with open('scratch/page_headers.txt', 'w', encoding='utf-8') as out:
    for fname in files:
        d = json.load(open(f'references/extracted/{fname}', encoding='utf-8'))
        txt = d.get('full_text', '')
        pages = txt.split('--- Page Break ---')
        out.write(f"=== {fname} (Total pages: {len(pages)}) ===\n")
        for i in range(min(5, len(pages))):
            lines = [l.strip() for l in pages[i].split('\n') if l.strip()]
            out.write(f"  Page {i+1} first 3 lines: {lines[:3]}\n")
            out.write(f"  Page {i+1} last 2 lines: {lines[-2:]}\n")
        out.write("\n")

print("Done writing scratch/page_headers.txt")
