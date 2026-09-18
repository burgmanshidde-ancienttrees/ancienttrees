import re
data = open('/tmp/hiroshima_kyoboku.html', encoding='shift_jis', errors='ignore').read()
text = re.sub('<[^>]+>', ' ', data)
text = re.sub(r'&nbsp;', ' ', text)
lines = [l.strip() for l in text.splitlines() if l.strip()]
joined = '\n'.join(lines)
for kw in ['東広島', '福富', '豊栄', '河内', '安芸津']:
    for m in re.finditer(kw, joined):
        s = max(0, m.start() - 150)
        e = min(len(joined), m.start() + 150)
        print('---', kw, '---')
        print(joined[s:e].replace(chr(10), ' | '))
        print()
