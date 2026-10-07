import json

data = json.load(open('references/all_extracted_details.json', encoding='utf-8'))

out_lines = []
for p in data:
    out_lines.append(f"==================================================")
    out_lines.append(f"[{p['id']}] {p['filename']} (DOI: {p['doi']})")
    out_lines.append(f"--------------------------------------------------")
    for i, l in enumerate(p['lines']):
        out_lines.append(f"{i:2d}: {l}")
    out_lines.append("")

with open('references/papers_readable.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print("Saved references/papers_readable.txt")
