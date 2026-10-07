import json
import re

files_to_check = [
    's00521-023-09033-7.json',
    's00521-024-10620-5.json',
    's11036-025-02465-6.json',
    's11047-025-10023-y.json',
    's13428-023-02062-z.json',
    's13677-025-00828-8.json'
]

with open('scratch/details_output.txt', 'w', encoding='utf-8') as out:
    for fname in files_to_check:
        d = json.load(open(f'references/extracted/{fname}', encoding='utf-8'))
        txt = d.get('full_text', '')
        out.write(f"=== {fname} ===\n")
        out.write(txt[:2000])
        out.write("\n" + "="*50 + "\n\n")

print("Written to scratch/details_output.txt")
