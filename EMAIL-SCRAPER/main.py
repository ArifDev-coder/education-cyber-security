from collections import deque
import re
from bs4 import BeautifulSoup
import requests
import urllib.parse

url= str(input("[+] Enter the url: "))
limit = int(input('Limit search (0 if not limit) : '))

urls = deque([url])
scrap_urls = set()
emails = set()
count = 0

try:
    while True:
        count += 1
        if count > limit:
            break
        u = urls.popleft()
        scrap_urls.add(u)
        parts = urllib.parse.urlsplit(u)
        b_url = f'{parts.scheme}://{parts.netloc}'
        path = u[:u.rfind('/')+1] if '/' in parts.path else u

        print(f'{count+1} Processing... {u}')
        
        try:
            #! error 
            res = requests.get(u)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue
        
        n_email = set(re.findall(r'[a-z0-9\.\-+_]+@\w+\.+[a-z\.]+', res.text, re.I))
        emails.update(n_email)

        s = BeautifulSoup(res.text, 'html.parser')
        for a in s.find_all('a'):
            link = a.attrs['href'] if 'href' in a.attrs else ''
            if link.startswith('/'):
                link = b_url + link
            elif not link.startswith('http'):
                link+=path
            
            if not link in urls and not link in scrap_urls:
                urls.append(link)

except KeyboardInterrupt:
    print('[-] Close...')
    break

print(f'\nProccess Done!')
print(f'\n{len(emails)} email found! \n*****************************************')
for mail in emails:
    print('   '+mail)
print('\n')