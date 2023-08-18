import json
from urllib.parse import urlparse, parse_qs

from mitmproxy import http


class ProxyLogger:
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


addons = [
    ProxyLogger()
]
