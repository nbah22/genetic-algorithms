from urllib.request import urlopen
from urllib.parse import urlencode
import json


key = "pdct.1.1.20140228T092352Z.a73414756c419f3d.39704a0939e94fa42781dd9e1bc9f98214e98ef1"
text = "test"
for i in range(30):
    params = urlencode([('key', key), ('lang', 'en'), ('q', text)])
    request = urlopen("https://predictor.yandex.net/api/v1/predict.json/complete?%s" % (params))
    result = json.loads(request.read().decode("utf-8", "strict"))
    if result['pos'] == 1:
        text += ' %s' % result['text'][0]
    else:
        text = text[:int(result['pos'])] + result['text'][0]
print(text)
