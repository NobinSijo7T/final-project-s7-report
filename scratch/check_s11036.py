import json

d = json.load(open('references/extracted/s11036-025-02465-6.json', encoding='utf-8'))
txt = d.get('full_text', '')
pages = txt.split('--- Page Break ---')
print("Page 1 full:")
print(pages[0][:1500])
