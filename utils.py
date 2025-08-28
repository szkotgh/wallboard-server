import os
from flask import request
import uuid

class ResultDTO:
    def __init__(self, code: int | bool, message: str, data=None, result: bool = False):
        self.code = code
        self.message = message
        self.data = data
        self.result = result

    def to_dict(self):
        return {'code': self.code, 'message': self.message, 'data': self.data}

    def to_response(self):
        return {'code': self.code, 'message': self.message, 'data': self.data}, self.code

def gen_hash(len: int) -> str:
    return os.urandom(16).hex()[:len]

def gen_uuid() -> str:
    return str(uuid.uuid4())

def get_request_ip(): 
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
    return f'{user_ip}'