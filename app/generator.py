#API = 'NDcxZmQ3YjMtMGQ2Mi00MTFmLWEyMjEtZmQ4NDA5N2FmNzBhOjkyNDU1Y2FhLTQzMzAtNDI2Ny1iMDYwLWY5NTg3OTM0N2MzOA=='

import requests

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload='scope=GIGACHAT_API_PERS'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': 'dc03d41c-c8f0-4b61-b0b0-848535de1ea7',
  'Authorization': 'Basic <NDcxZmQ3YjMtMGQ2Mi00MTFmLWEyMjEtZmQ4NDA5N2FmNzBhOjkyNDU1Y2FhLTQzMzAtNDI2Ny1iMDYwLWY5NTg3OTM0N2MzOA==>'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)