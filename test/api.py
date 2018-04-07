import requests
import sys

s = requests.Session()

print('Testing client GET: http://127.0.0.1:8080/api/client')
r = s.get('http://127.0.0.1:8080/api/client')
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing client POST: http://127.0.0.1:8080/api/client')
json_in={   "name":"Goku",
            "email":"songoku@ssj.god",
            "cep":"76541-222",
            "phone1":"(19)31257164",
            "phone2":None,
            "cpf":"11122233355",
            "password":"kakaroto",
            "birthday":"09091209",
            "sex":None
            }
        
r = s.post('http://127.0.0.1:8080/api/client', json=json_in)
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))
if r.status_code == 500:
    sys.exit(0)
result = r.json()
client_id = result["Client ID"]

print('Testing client GET: http://127.0.0.1:8080/api/client?clientid={}'.format(client_id))
r = s.get('http://127.0.0.1:8080/api/client', params={"clientid":client_id})
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing client PUT: http://127.0.0.1:8080/api/client')
r = s.put('http://127.0.0.1:8080/api/client')
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing UserAccess POST: http://127.0.0.1:8080/api/useraccess')
r = s.post('http://127.0.0.1:8080/api/useraccess', json={"email": json_in["email"], "password": json_in["password"]})
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))
if r.status_code == 500:
    sys.exit(0)
result = r.json()
token = result['token']

print('Testing UserAccess GET: http://127.0.0.1:8080/api/useraccess')
r = s.get('http://127.0.0.1:8080/api/useraccess', params={'token':token})
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

print('Testing client DELETE: http://127.0.0.1:8080/api/client?clients={}'.format(client_id))
r = s.delete('http://127.0.0.1:8080/api/client', params={'clientid':client_id})
print('Status: %s\nReturn: %s\n' % (r.status_code, r.text))

