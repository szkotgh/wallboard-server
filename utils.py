import os
from flask import request
import uuid
import ipaddress

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

def mask_ip_address(ip_str: str) -> str:
    """
    IP 주소를 마스킹 처리합니다.
    IPv4: 마지막 옥텟을 마스킹 (예: 192.168.1.xxx)
    IPv6: 마지막 32비트를 마스킹 (예: 2001:db8::xxxx:xxxx)
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        if ip.version == 4:
            # IPv4: 마지막 옥텟을 xxx로 마스킹
            ip_parts = str(ip).split('.')
            return f"{'.'.join(ip_parts[:-1])}.xxx"
        else:
            # IPv6: 마지막 32비트를 xxxx:xxxx로 마스킹
            ip_str = str(ip)
            if '::' in ip_str:
                # 축약된 형태인 경우
                parts = ip_str.split('::')
                if len(parts) == 2 and parts[1]:
                    # :: 뒤에 부분이 있는 경우
                    last_parts = parts[1].split(':')
                    if len(last_parts) >= 2:
                        return f"{parts[0]}::xxxx:xxxx"
                    else:
                        return f"{parts[0]}::xxxx"
                else:
                    # ::만 있는 경우
                    return f"{parts[0]}::xxxx:xxxx"
            else:
                # 전체 형태인 경우
                parts = ip_str.split(':')
                if len(parts) >= 8:
                    return f"{':'.join(parts[:-2])}:xxxx:xxxx"
                else:
                    return f"{':'.join(parts[:-1])}:xxxx"
    except ValueError:
        # IP 주소 파싱 실패 시 원본 반환
        return ip_str