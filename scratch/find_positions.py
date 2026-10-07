import os

# Let's inspect the exact lines in main.tex where Chapter 2 starts and ends
with open('main.tex', 'r', encoding='utf-8') as f:
    content = f.read()

chap2_start = content.find('\\chapter{Literature Review}')
chap3_start = content.find('\\chapter{System Requirements and Architecture Specification}')
bib_start = content.find('\\begin{thebibliography}{99}')
bib_end = content.find('\\end{thebibliography}')

print(f"Chap 2 index: {chap2_start} to {chap3_start}")
print(f"Bib index: {bib_start} to {bib_end}")
