import json
from io import BytesIO

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


def download(fs_id, dest: BytesIO = None, sleep_time: int = 3):
    """
    Download the file from Terabox.

    :param sleep_time: time browser need to send requests. Increase this parameter if sign.json won't update
    :param fs_id: file id, obtained from `Uploader.upload()` function.
    :param dest: optional, BytesIO object where the file data would be downloaded.
    :return: name of the downloaded file.
    """
    url = f'https://www.terabox.com/api/download'

    headers = Uploader.headers
    cookies = Uploader.parse_cookie_file()

    params = get_params(fs_id)
    response = requests.get(url, headers=headers, params=params, cookies=cookies)
    response_data = json.loads(response.content)
    errno = response_data['errno']
    while errno != 0:
        print(f"Sign parameter is outdated. Errno: {errno}. Running the sign updating...")
        update_sign(sleep_time)
        params = get_params(fs_id)
        response = requests.get(url, headers=headers, params=params, cookies=cookies)
        response_data = json.loads(response.content)
        errno = response_data['errno']

    if len(response_data['dlink']) == 0:
        raise Exception("fs_id is invalid. Picture wasn't found on the server")
    link = response_data['dlink'][0]['dlink']

    response_file = requests.get(link, headers=headers, cookies=cookies)
    filename = response_file.headers['Content-Disposition'][21:-1]

    if dest is None:
        with open(filename, "wb") as file:
            file.write(response_file.content)
    else:
        dest.write(response_file.content)
        return filename
