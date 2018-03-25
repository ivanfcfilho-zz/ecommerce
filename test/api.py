import requests

s = requests.Session()

print('Testing client GET: http://127.0.0.1:8080/api/client')
r = s.get('http://127.0.0.1:8080/api/client')
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing client POST: http://127.0.0.1:8080/api/client')
r = s.post('http://127.0.0.1:8080/api/client')
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing client DELETE: http://127.0.0.1:8080/api/client')
r = s.delete('http://127.0.0.1:8080/api/client')
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing client PUT: http://127.0.0.1:8080/api/client')
r = s.put('http://127.0.0.1:8080/api/client')
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing UserAccess GET: http://127.0.0.1:8080/api/useraccess')
r = s.get('http://127.0.0.1:8080/api/useraccess')
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing UserAccess POST: http://127.0.0.1:8080/api/useraccess')
r = s.post('http://127.0.0.1:8080/api/useraccess')
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))
