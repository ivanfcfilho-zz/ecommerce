import requests
import simplejson
import jwt

s = requests.Session()

print('Testing client GET: http://127.0.0.1:8080/api/client')
r = s.get('http://127.0.0.1:8080/api/client')
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing client POST: http://127.0.0.1:8080/api/client')
json_in={   "name": "Goku",
            "email": "songoku@email.com",
            "cep": "76541-222",
            "phone1": "(19)31257164",
            "cpf": "11122233355",
            "password": "kakaroto",
            "birthday": "09091209"
        }
        
r = s.post('http://127.0.0.1:8080/api/client', json=json_in)
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing client PUT: http://127.0.0.1:8080/api/client')
r = s.put('http://127.0.0.1:8080/api/client')
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing UserAccess POST: http://127.0.0.1:8080/api/useraccess')
r = s.post('http://127.0.0.1:8080/api/useraccess', json={"email": "songoku@email.com", "password": "kakaroto"})
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))
token = r.text

print('Testing UserAccess GET: http://127.0.0.1:8080/api/useraccess')
r = s.get('http://127.0.0.1:8080/api/useraccess', params={'token':token})
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing client DELETE: http://127.0.0.1:8080/api/client?clients=9')
r = s.delete('http://127.0.0.1:8080/api/client', params={'clients':6})
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))
