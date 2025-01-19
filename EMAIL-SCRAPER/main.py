from collections import deque
import re
from bs4 import BeautifulSoup
import requests
import urllib.parse

url = str(input("[+] Enter the url: "))
limit = int(input('Limit search (0 if not limit): '))

urls = deque([url])
scrap_urls = set()
emails = set()
count = 0

# Helper function to check if a URL is valid
def is_valid_url(url):
    # Skip javascript and hash fragment links
    if url.startswith(('javascript:', '#')) or not url:
        return False
    return url.startswith(('http', 'https', 'ftp'))

try:
    while True:
        count += 1
        if count > limit:
            break
        u = urls.popleft()
        scrap_urls.add(u)
        
        # Split the URL to handle the fragment part
        parts = urllib.parse.urlsplit(u)
        base_url = f'{parts.scheme}://{parts.netloc}'
        path = u[:u.rfind('/')+1] if '/' in parts.path else u

        # Ignore fragment part (e.g., '#carousel')
        u_without_fragment = urllib.parse.urlunsplit(parts._replace(fragment=""))

        print(f'{count} Processing... {u_without_fragment}')
        
        try:
            res = requests.get(u_without_fragment)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
            continue
        
        # Extract emails
        n_email = set(re.findall(r'[a-z0-9\.\-+_]+@\w+\.+[a-z\.]+', res.text, re.I))
        emails.update(n_email)

        s = BeautifulSoup(res.text, 'html.parser')
        for a in s.find_all('a'):
            link = a.attrs['href'] if 'href' in a.attrs else ''
            
            # Handle relative links
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            
            # Ensure no fragments are included in the new link
            link_parts = urllib.parse.urlsplit(link)
            link_without_fragment = urllib.parse.urlunsplit(link_parts._replace(fragment=""))
            
            # Skip invalid URLs (e.g., javascript:void(0), # links)
            if not is_valid_url(link_without_fragment) or link_without_fragment in urls or link_without_fragment in scrap_urls:
                continue

            urls.append(link_without_fragment)

except KeyboardInterrupt:
    print('[-] Close...')

print(f'\nProcess Done!')
print(f'\n{len(emails)} email found! \n*****************************************')
for mail in emails:
    print('   ' + mail)
print('\n')
