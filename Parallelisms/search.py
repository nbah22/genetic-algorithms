import re
import urllib
from urllib.request import Request
from urllib.parse import urlencode


text = "test"
multipliers = {
    '': 1,
    'млн': 10 ** 6,
    'тыс.': 10 ** 3
}
params = urlencode([('text', text)])

# request = urlopen("http://yandex.ru/yandsearch?%s" % (params))
# source = request.read().decode("utf-8", "strict")

request = Request("http://yandex.ru/yandsearch?%s" % (params))
request.add_header('cookie',
                   'Session_id=2:1395410589.0.5.25862341.8:1395410589000:3260411402:6.0.1.1.0.107643.856713.dd5914f6e8407930e25a5986fd092e4e')
request.add_header('cookie', 'my=YzYBAQA=')
request.add_header('cookie', 'yandexuid=739693031395413508')
request.add_header('cookie',
                   'fuid01=532c4b2d1f993a2c.OKMGT4o8ihTwK--3YTBDASX4UMPIwIr3XLWQpJF1geX3vplR4_T5bbyL1foIVEqhqocdwiK7fmeI5K3i0d4Xre1rw2ta-0AS641t1YywYof3E2i4Xalgzou0kU5vznmS')
request.add_header('cookie',
                   'spravka=dD0xMzk1NDEzMzgxO2k9MTk0Ljg1LjIzOC4xMDt1PTEzOTU0MTMzODE2OTkzMjgzODk7aD0xNGYzYmEwY2YwYWI5N2QwZmZjMWI5MjM1YWQyNTgwYg==')
request.add_header('cookie',
                   'L=D24ocWVyYQR6fABVDGJcU0BbYgBYX0cIYx85YDc2E1pWBhI0eys6LlErRVBeTGcwLnQaJkw7VQ5YRQR1TxRFJg==.1395410589.10336.248593.efb89109f25d30934e507e58ba9df9aa')
opener = urllib.request.build_opener()
source = opener.open(request).read().decode("utf-8", "strict")

print(source)
result = re.search("Яндекс: нашлось (\d+) ?(\w*) ответ", source).group(1, 2)
fitness = int(result[0]) * multipliers[result[1]]
print(fitness)
