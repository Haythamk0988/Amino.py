import hmac
import json
import os

from functools import reduce
from base64 import b64decode, b64encode
from hashlib import sha1

def generate_device_id() -> str:
    identifier = os.urandom(20)
    key = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")
    mac = hmac.new(key, bytes.fromhex("42") + identifier, sha1)
    return f"42{identifier.hex()}{mac.hexdigest()}".upper()

def generate_signature(data) -> str:
    try: d = data.encode("utf-8")
    except Exception: d = data

    mac = hmac.new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"), d, sha1)
    return b64encode(bytes.fromhex("42") + mac.digest()).decode("utf-8")

def generate_device_info():
    return {
        "device_id": generate_device_id(),
        "user_agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.5.33562)"
    }

# okok says: please use return annotations :(( https://www.python.org/dev/peps/pep-3107/#return-values

def decode_sid(sid: str) -> dict:
    return json.loads(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), sid + "=" * (-len(sid) % 4)).encode())[1:-20].decode())

def sid_to_uid(SID: str) -> str: return decode_sid(SID)["2"]

def sid_to_ip_address(SID: str) -> str: return decode_sid(SID)["4"]