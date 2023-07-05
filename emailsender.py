import requests


def sendEmail(email, name, alerts):
    url = "https://api.courier.com/send"

    lines = ""
    for line in alerts:
        lines += f"{line}\n"

    payload = {
        "message": {
            "template": "",  # template id
            "to": {
                "email": email,
                "data": {
                    "name": name,
                    "alerts": lines
                }
            }
        }
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": ""  # authorization token thing
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.text
