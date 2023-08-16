from Uploader import Uploader
from download import download

if __name__ == "__main__":
    filename = "storage/monster2.png"
    uploader = Uploader(filename)
    fs_id = uploader.upload()
    # fs_id = 51794494215547
    print(fs_id)
    download(fs_id)
