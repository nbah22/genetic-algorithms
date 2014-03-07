import re
import urllib
from urllib.request import Request
from urllib.parse import urlencode


text = "test"
multipliers = {
    'млн': 10 ** 6,
    'тыс.': 10 ** 3
}
params = urlencode([('text', text)])

# request = urlopen("http://yandex.ru/yandsearch?%s" % (params))
# source = request.read().decode("utf-8", "strict")

request = Request("http://yandex.ru/yandsearch?%s" % (params))
request.add_header('User-Agent', '')
opener = urllib.request.build_opener()
source = opener.open(request).read().decode("utf-8", "strict")

print(source)
result = re.search("Яндекс: нашлось (\d+) (\w+) ответ", source).group(1, 2)
fitness = int(result[0]) * multipliers[result[1]]
print(fitness)
print(text)
