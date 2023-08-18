import json
from urllib.parse import urlparse, parse_qs

from mitmproxy import ctx, http


class ProxyLogger:
    def __init__(self):
        self.log_file = open("proxy_log.txt", "a")

    def response(self, flow: http.HTTPFlow) -> None:
        request_url = flow.request.url
        query = urlparse(request_url).query
        params = parse_qs(query)
        if "sign" in params and "timestamp" in params:
            sign = params["sign"][0]
            timestamp = params["timestamp"][0]
            clear_dict = {"sign": sign,
                          "timestamp": timestamp}
            with open("sign.json", "w") as file:
                json.dump(clear_dict, file)

        response_status_code = flow.response.status_code
        log_entry = f"Request URL: {request_url} | Response Status Code: {response_status_code}\n"
        self.log_file.write(log_entry)
        self.log_file.flush()


    def done(self):
        self.log_file.close()
        pass


addons = [
    ProxyLogger()
]
