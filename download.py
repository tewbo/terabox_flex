import json
from Uploader import Uploader

import requests


def download(fs_id):
    url = f'https://www.terabox.com/api/download'
    params = {
        'fidlist': f'[{fs_id}]',
        'sign': '90gebcUMSGn3UzxIU1LH9V1+q2Twbz6FKUC+3sIJsH5mQZSiJHeE0Q==', # it may need to be changed, idk
        'timestamp': '1692148645'
    }
    headers = Uploader.headers
    cookies = Uploader.parseCookieFile()

    response = requests.get(url, headers=headers, params=params, cookies=cookies)
    print(response.status_code)
    response_data = json.loads(response.content)
    link = response_data['dlink'][0]['dlink']
    print(link)

    response_file = requests.get(link, headers=headers, cookies=cookies)
    filename = response_file.headers['Content-Disposition'][21:-1]
    with open(filename, "wb") as file:
        file.write(response_file.content)

