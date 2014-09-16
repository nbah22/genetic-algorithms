import xml.etree.ElementTree as ET
from urllib.request import urlopen
from urllib.parse import urlencode


user = "Nbah22"
key = "03.25862341:ba4597add0fb3bee1ccc9ab4e832c9ab"
query = "yessdf"
params = urlencode([('user', user), ('key', key), ('query', query)])
request = urlopen("http://xmlsearch.yandex.ru/xmlsearch?%s" % params)
text = request.read().decode("utf-8", "strict")
root = ET.fromstring(text)

print(root[1][2].text)  # approximate
print(root[1][5][0][4].text)  # more accurate
print(int(root[1][2].text) / int(root[1][5][0][4].text))
