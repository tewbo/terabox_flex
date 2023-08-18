import json
import re
from io import BytesIO

import requests


class Uploader:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.5481.78 Safari/537.36',
        'Origin': 'https://www.terabox.com',
        'Referer': 'https://www.terabox.com/russian/main?category=all',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-EN,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    cookies_file = "cookies.txt"

    def __init__(self, filename: str, file_io: BytesIO):
        self.filename = filename
        self.file_io = file_io
        self.file_io.seek(0)
        self.sess = requests.Session()
        self.cookies = self.parse_cookie_file()

    @staticmethod
    def parse_cookie_file():
        cookies = {}
        with open(Uploader.cookies_file, 'r') as fp:
            for line in fp:
                if not re.match(r'^#', line):
                    line_fields = line.strip().split('\t')
                    cookies[line_fields[5]] = line_fields[6]
        return cookies

    def precreate(self):
        url = 'https://www.terabox.com/api/precreate'
        data = {
            'path': f'/{self.filename}',
            'autoinit': '1',
            'target_path': '/',
            'block_list': '["5910a591dd8fc18c32a8f3df4fdc1761"]',
            'local_mtime': '1692132182'
        }

        response = self.sess.post(url, headers=self.headers, data=data, cookies=self.cookies)
        return response

    def data_upload(self, upload_id):
        url = f"https://c-jp.terabox.com/rest/2.0/pcs/superfile2"
        params = {
            'method': 'upload',
            'app_id': '250528',
            'channel': 'dubox',
            'clienttype': '0',
            'web': '1',
            'logid': 'MTY5MjEzMjE1NDA5NzAuMTgwNjcwMTYwMzc0NDM3NjI=',
            'path': f'/{self.filename}',
            'uploadid': upload_id,
            'uploadsign': '0',
            'partseq': '0',
        }
        changed_headers = self.headers.copy()
        changed_headers['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundaryBhYLzy0AIqJ0DRQN'
        data = (
                b'------WebKitFormBoundaryBhYLzy0AIqJ0DRQN\r\n'
                b'Content-Disposition: form-data; name="file"; filename="blob"\r\n'
                b'Content-Type: application/octet-stream\r\n\r\n'
                + self.file_io.read() +
                b'\r\n------WebKitFormBoundaryBhYLzy0AIqJ0DRQN--'
        )
        response = self.sess.post(url, headers=changed_headers, params=params, data=data, cookies=self.cookies)
        return response

    def create(self, block_list, upload_id):
        url = 'https://www.terabox.com/api/create'
        self.file_io.seek(0)
        data_encoded = {
            'path': f'/{self.filename}',
            'size': str(len(self.file_io.read())),
            'uploadid': upload_id,
            'block_list': block_list
        }

        response = self.sess.post(url, headers=self.headers, data={**data_encoded}, cookies=self.cookies)
        return response

    def upload(self) -> int:
        """
        :return: fs_id - unique identifier, needed to download this picture.
        """
        r1 = self.precreate()
        r1_map = json.loads(r1.content)
        upload_id = r1_map["uploadid"]

        r2 = self.data_upload(upload_id)
        r2_map = json.loads(r2.content)

        r3 = self.create(f'["{r2_map["md5"]}"]', upload_id)
        r3_map = json.loads(r3.content)

        return r3_map['fs_id']
