from Uploader import Uploader
from download import download

if __name__ == "__main__":
    filename = "storage/espresso.jpg"
    uploader = Uploader(filename)
    fs_id = uploader.upload()
    print(fs_id)
    download(fs_id)
