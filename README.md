# terabox-flex
**Unofficial API to download and upload file to Terabox**

## Installing
1. Obtain *cookies.txt extension* from here: https://github.com/death-angel-141/cookies.txt
2. Put cookies to *cookies.txt* file in root directory
3. Install requirements.txt
4. Run ***mitmproxy***:
    ``` bash
    $ mitmproxy -s proxy.py -p 8090
    ```
5. Install Google Chrome if you don't have it.

## Usage example
``` python
file_io = BytesIO()
with open("example.png", "rb") as file:
  file_io.write(file.read())
uploader = Uploader("example.png", file_io)
fs_id = uploader.upload()  # upload file and get its unique id in terabox

result = BytesIO()
download(fs_id, result) # download file to the bytesIO object and now we can save it or do smth else
```

## Other
- You need to have at least one file in root directory in your Terabox cloud.
- It may be troubles with button title on Terabox in different languages.
- You can upload your files to a directory on the Terabox, if you specify it in filename like
  ``` python
   filename = "/my_dir/example.png"
  ```
- If your `sign.json` won't update, try to increase SLEEP_TIME parameter in `browser_pass.py`




