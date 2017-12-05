import requests

url = 'http://117.27.136.53:8081/getresource.svd?domain=getyunyuebooklist&appid=641cacd8-af0a-4987-9285-200ed4733b95'

print requests.get(url).text
