import base64
import hashlib
import hmac
import os
import requests
import json
from pydantic import BaseModel



class LineModel():
    def __init__(self):
        self.CHANNEL_SECRET="XXXXX"
        self.CHANNEL_ACCESS_TOKEN="XXXXX"
        self.headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.CHANNEL_ACCESS_TOKEN}"
        }

    def signatureValidation(self,signature, body_json)-> bool:
        print(f"body_json={body_json}")
        print(self.CHANNEL_SECRET)
        print(self.CHANNEL_ACCESS_TOKEN)
        hash = hmac.new(self.CHANNEL_SECRET.encode('utf-8'),
            body_json.encode('utf-8'), hashlib.sha256).digest()
        signatureCal = base64.b64encode(hash)
        signature=signature.encode('utf-8')
        print(f"hash={hash}")
        print(f"signatureCal={signatureCal}")
        print(f"signature={signature}")
        # Compare x-line-signature request header and the signature
        return hmac.compare_digest(signature, signatureCal)


    def replyMessage(self,token,payload):
        url = "https://api.line.me/v2/bot/message/reply"

        payload = json.dumps({
        "replyToken": f"{token}",
        "messages": payload
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)
        print(response.text)

    def loadMessage(self,userId):
        url = "https://api.line.me/v2/bot/chat/loading/start"

        payload = json.dumps({ "chatId": f"{userId}" })
        response = requests.request("POST", url, headers=self.headers, data=payload)
        print(response.text)


if __name__ == "__main__":
    signature = ""
    body_json = {'jsonKey': 'jsonValue',"title": "hello world"}
    line_request = LineModel()
    validate = line_request.signatureValidation(signature,body_json)