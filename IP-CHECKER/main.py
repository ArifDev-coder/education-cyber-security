import socket
import requests
import pprint
import json

hostname = input('Enter a domain name: ')
ip_addreas = socket.gethostbyname(hostname)

request_url = f'https://geolocation-db.com/jsonp/{ip_addreas}'
response = requests.get(request_url)
geolocation = response.content.decode()
geolocation = geolocation.split("(")[1].strip(")")
geolocation = json.loads(geolocation)
for k,v in geolocation.items():
    pprint.pprint(str(k)+' : '+ str(v))

print(f'Domain Name: {hostname}')
print(f'IP Addreas: {ip_addreas}')