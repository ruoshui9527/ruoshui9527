import requests
from time_util import wait_time

def is_valid_proxy(url, headers):
    while True:
        retry_count = 5
        proxy = get_proxy().get("proxy")
        valid_proxy = None
        response_text = None
        while retry_count > 0 and proxy:
            try:
                response = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
                response.raise_for_status()
                valid_proxy = proxy
                response_text = response.text
                break
            except requests.exceptions.RequestException:
                retry_count -= 1

        if valid_proxy:
            return response_text
        else:
            del_proxy(proxy)

        wait_time()


def get_proxy():
    return requests.get("http://192.168.1.10:5010/get").json()


def del_proxy(proxy):
    requests.get("http://192.168.1.10:5010/delete/?proxy={}".format(proxy))