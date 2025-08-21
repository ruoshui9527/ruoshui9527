from yunhu.openapi import Openapi

def send_message(links):
    for link in links:
        content = {
            "text": link[1],
            "buttons": [
                [{
                    "text": "点击跳转原文",
                    "actionType": 1,
                    "url": link[0]
                }]
            ]
        }

        openapi = Openapi("token")
        openapi.sendMessage("9527", "user", "text", content)