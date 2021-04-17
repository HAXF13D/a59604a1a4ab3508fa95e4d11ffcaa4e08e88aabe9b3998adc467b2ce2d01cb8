from config import tg_token, HEADERS
import requests
import json
import base64
from Functions import get_file_name, get_chat_id, add_file

from Txt_Const import DONE_MSG

files = []


def export_id(templateid, data):
    response = requests.post(f"https://fastreport.cloud/api/rp/v1/Templates/File/{templateid}/Export",
                             headers=HEADERS,
                             data=data)

    expId = response.content.decode("UTF-8")
    expId = json.loads(expId)
    expId = expId["id"]
    return expId


def get_root_folder(file_name):
    response = requests.get("https://fastreport.cloud/api/rp/v1/Exports/Root", headers=HEADERS)
    derId = response.content.decode("UTF-8")
    derId = json.loads(derId)
    derId = derId["id"]
    name = get_file_name(file_name)
    return name, derId


def file_folder(rootid, file_name):
    url = files[-1].file_url
    file = requests.get(url).text
    file = base64.b64encode(bytes(file, "UTF-8"))
    file = file.decode("UTF-8")
    data = {
        "name": file_name,
        "content": str(file)
    }
    data = json.dumps(data)
    response = requests.post(f"https://fastreport.cloud/api/rp/v1/Templates/Folder/{rootid}/File", headers=HEADERS,
                             data=data)
    return response


def set_connection():
    response = requests.get("https://fastreport.cloud/api/rp/v1/Templates/Root?subscriptionId=60793a337648280001cd3514",
                            headers=HEADERS)
    rootId = response.content.decode("UTF-8")
    rootId = json.loads(rootId)
    rootId = rootId["id"]
    return rootId


def misha_func():

    while True:
        if not len(files) == 0:
            rootId = set_connection()
            user_id = files[-1].user_id
            file_name = files[-1].file_name
            response = file_folder(rootId, file_name)
            add_file(user_id)
            templateId = response.content.decode("UTF-8")
            templateId = json.loads(templateId)
            templateId = templateId["id"]

            name, derId = get_root_folder(file_name)

            data = {
                "fileName": f"{name}.pdf",
                "folderId": derId,
                "format": "Pdf",
            }
            data = json.dumps(data)

            expId = export_id(templateId, data)

            while True:
                response = requests.get(f"https://fastreport.cloud/api/rp/v1/Exports/File/{expId}", headers=HEADERS)
                result = response.content.decode("UTF-8")
                result = json.loads(result)
                resultId = result["id"]
                if result["status"] == "Success":
                    print(resultId)
                    response = requests.get(f"https://fastreport.cloud/download/e/{resultId}", headers=HEADERS, stream=True)
                    file_bytes = response.content
                    break

            requests.delete(f"https://fastreport.cloud/api/rp/v1/Templates/File/{templateId}", headers=HEADERS)

            chat_id = get_chat_id(user_id)
            url = f"https://api.telegram.org/bot{tg_token}/sendDocument"
            data = {
                'chat_id': chat_id,
                'caption': DONE_MSG
            }

            response = requests.post(url=url, data=data, files={'document': (f"{name}.pdf", file_bytes)})
            print(response.content)


class Files:

    def __init__(self, file_number, file_name, file_url, user_id):
        self.number = file_number
        self.file_name = file_name
        self.user_id = user_id
        self.file_url = file_url
        self.status = "NOT_DONE"

    def change_status(self, status):
        self.status = status
