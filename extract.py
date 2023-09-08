import http.client

conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 5ReoJ0rm1bpGaK0FshmvcX:3KtLSLfVclRlsnJty2xR1n"
    }

conn.request("GET", "https://api.collectapi.com/economy/hisseSenedi", headers=headers)

res = conn.getresponse()
data = res.read()

jsonString = data.decode("utf-8")
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()