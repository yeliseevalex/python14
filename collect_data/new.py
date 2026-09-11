import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Mobile Safari/537.36',
    'Referer': 'https://www.rottentomatoes.com/browse/movies_at_home?page=8',
}

params = {
    'after': 'Mjg5',
}

response = requests.get('https://www.rottentomatoes.com/cnapi/browse/movies_at_home', params=params, headers=headers)
print(response.json())

# import base64
# print(base64.b64decode("MjAw"))
# print(base64.b64decode("MjI5"))