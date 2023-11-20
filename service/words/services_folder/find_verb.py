import requests
from bs4 import BeautifulSoup

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

word = input()
url = f"https://verbformen.de/?w={word}"

req = requests.get(url, headers=headers)

with open('new.html', 'w+') as f:
    f.write(req.text)

src = ''

with open('./new.html', 'r') as f:
    src = f.read()

soup = BeautifulSoup(src, 'lxml')

section = soup.find("section", {"id": "vVdBxBox"})

res = []

for i in section.children:
    if i.name == 'p' and i.text != '\n':
        res.append(i.text)

for i in res:
    res.append(" ".join(i.split()))
    res.remove(i)

print(res)
