import json
import re

for fname in ['s11036-025-02465-6.json', 's11047-025-10023-y.json', 's13677-025-00828-8.json', 's00521-023-09033-7.json', 's00521-024-10620-5.json', 's13428-023-02062-z.json']:
    d = json.load(open(f'references/extracted/{fname}', encoding='utf-8'))
    txt = d.get('full_text', '')
    print(f"***** {fname} *****")
    # let's look at equations or warnings or first 5000 chars
    print("Num pages:", d.get('num_pages'))
    # search for 'doi.org' or title patterns
    for m in re.finditer(r'(?:title|journal|doi|vol).*', txt[:3000], re.IGNORECASE):
        print("  Match:", m.group(0)[:100])
