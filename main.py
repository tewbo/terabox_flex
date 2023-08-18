from io import BytesIO

from Uploader import Uploader
from download import download

if __name__ == "__main__":
    filename = "monster.png"
    file_io = BytesIO()
    with open(filename, "rb") as file:
        file_io.write(file.read())
    uploader = Uploader(filename, file_io)
    fs_id = uploader.upload()
    print(fs_id)
    result = BytesIO()
    download(fs_id, result)
    with open("kek.jpg", "wb") as file:
        result.seek(0)
        file.write(result.read())
