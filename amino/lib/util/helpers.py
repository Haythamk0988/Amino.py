import hmac
import json
import os

from base64 import b64encode, urlsafe_b64decode
from hashlib import sha1

def generate_device_id() -> str:
    identifier = os.urandom(20)
    key = bytes.fromhex("AE49550458D8E7C51D566916B04888BFB8B3CA7D")
    mac = hmac.new(key, bytes.fromhex("52") + identifier, sha1)
    return f"52{identifier.hex()}{mac.hexdigest()}".upper()

def generate_signature(data) -> str:
    try: d = data.encode("utf-8")
    except Exception: d = data

    mac = hmac.new(bytes.fromhex("EAB4F1B9E3340CD1631EDE3B587CC3EBEDF1AFA9"), d, sha1)
    return b64encode(bytes.fromhex("52") + mac.digest()).decode("utf-8")

def generate_device_info():
    return {
        "device_id": generate_device_id(),
        "user_agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/star2ltexx-user 7.1.; com.narvii.amino.master/3.4.33602"
    }

# okok says: please use return annotations :(( https://www.python.org/dev/peps/pep-3107/#return-values

def decode_sid(sid: str) -> dict:
    return json.loads(urlsafe_b64decode(sid + "=" * (4 - len(sid) % 4))[1:-20])

def sid_to_uid(SID: str) -> str: return decode_sid(SID)["2"]

def sid_to_ip_address(SID: str) -> str: return decode_sid(SID)["4"]

def sid_created_time(SID: str) -> str: return decode_sid(SID)["5"]

def sid_to_client_type(SID: str) -> str: return decode_sid(SID)["6"]
