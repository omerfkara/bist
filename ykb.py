'''from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus
url = 'https://api.yapikredi.com.tr/api/stockmarket/v1/stockInformation'
queryParams = '?' + urlencode({ quote_plus('type') : 'MOST_TRADED'  })
request = Request(url + queryParams)
request.get_method = lambda: 'GET'
response_body = urlopen(request).read()
print response_body
'''

import requests

# The API endpoint
url = "https://jsonplaceholder.typicode.com/posts/1"
url = 'https://api.yapikredi.com.tr/api/stockmarket/v1/stockInformation?type=MOST_TRADED'

# A GET request to the API
response = requests.get(url)
print(response.text)

"""
{'userId': 1, 'id': 1, 'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit', 'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'}
"""