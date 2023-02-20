import requests
import base64

url = 'http://localhost/vdk/hs/test_http/huistring_line?message=nenavizhu1c'

req = requests.get(url, auth =('tg_bot', '123'))

print(req.status_code)
print(req.headers)
print(req.text)