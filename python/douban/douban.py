from collections import deque

from bs4 import BeautifulSoup
from proxy_pool import is_valid_proxy
from send_message import send_message

MAX_SIZE = 100

previous_link = deque(maxlen=MAX_SIZE)

m_url = "https://m.douban.com/group/CDzufang/"
m_headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

pc_url = "https://www.douban.com/group/CDzufang/"
pc_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
}

def get_douban(argument):
    response_text = None
    if argument == "m":
        response_text = is_valid_proxy(m_url, m_headers)
        m_parse(response_text)
    else:
        response_text = is_valid_proxy(pc_url, pc_headers)
        pc_parse(response_text)

def m_parse(response_text):
    soup = BeautifulSoup(response_text, "html.parser")

    tables = soup.find_all("ul", {"class": "base-list topic-list"})

    current_links = set()

    for table in tables:
        links = table.find_all("a")
        for link in links:
            href = "https://m.douban.com"+link["href"]
            title = link["title"]
            current_links.add((href, title))
    send(current_links)


def pc_parse(response_text):
    soup = BeautifulSoup(response_text, "html.parser")

    tables = soup.find_all("td", {"class": "title"})

    current_links = set()

    for table in tables:
        link = table.find("a")
        if link:
            href = link["href"]
            title = link.text.strip()
            current_links.add((href, title))
    send(current_links)


def send(current_links):
    new_links = set(current_links) - set(previous_link)
    if new_links:
        previous_link.extend(current_links)
        send_message(new_links)


