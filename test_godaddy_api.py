import requests
import orjson as json
from requests.structures import CaseInsensitiveDict

with open("login_creds.json", "rb") as login_creds:
    login_creds = json.loads(login_creds.read())

authorization = "sso-key " + login_creds["godady_api_login"]["key"] + ":" + login_creds["godady_api_login"]["secret"]

url = "https://api.ote-godaddy.com/v1/domains/available?checkType=full"

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["Content-Type"] = "application/json"
headers["Authorization"] = authorization

data = """
[
  "identitydesign.com", "masayukikishi.com", "google.com", "ginlet.com"
]
"""


resp = requests.post(url, headers=headers, data=data)

print(resp.text)
