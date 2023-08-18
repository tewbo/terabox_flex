import json
from Uploader import Uploader
from browser_pass import update_sign
import requests


def get_params(fs_id):
    with open("sign.json", "r") as file:
        sign_json = json.load(file)
    params = {
        'fidlist': f'[{fs_id}]',
        'sign': sign_json['sign'],
        'timestamp': sign_json['timestamp'],
    }
    return params


def download(fs_id):
    url = f'https://www.terabox.com/api/download'

    headers = Uploader.headers
    cookies = Uploader.parseCookieFile()

    params = get_params(fs_id)
    response = requests.get(url, headers=headers, params=params, cookies=cookies)
    response_data = json.loads(response.content)
    errno = response_data['errno']
    while errno != 0:
        print(f"Ошибка при скачивании файла. Вероятно, протух sign. Errno: {errno}")
        update_sign()
        params = get_params(fs_id)
        response = requests.get(url, headers=headers, params=params, cookies=cookies)
        response_data = json.loads(response.content)
        errno = response_data['errno']

    if len(response_data['dlink']) == 0:
        raise Exception("У вас неправильный fs_id, картинка не найдена на сервере")
    link = response_data['dlink'][0]['dlink']

    response_file = requests.get(link, headers=headers, cookies=cookies)
    filename = response_file.headers['Content-Disposition'][21:-1]
    with open(filename, "wb") as file:
        file.write(response_file.content)
