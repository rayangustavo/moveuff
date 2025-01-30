import logging
import requests
from hashlib import sha3_256
from os import environ

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]

def hex2str(hex):
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    return "0x" + str.encode("utf-8").hex()

def get_function_selector(function_signature):
    keccak = sha3_256()
    keccak.update(function_signature.encode('utf-8'))
    return keccak.digest()[:4]


def add_notice(notice):
    try:
        notice = str2hex(notice)
        logger.info("Adding notice")
        response = requests.post(rollup_server + "/notice", json={"payload": notice})
        logger.info(f"Received notice status {response.status_code} body {response.content}")
    except Exception:
        logger.error("Error creating notice.")

    return

def add_voucher(voucher):
    try:
        logger.info(f"Adding voucher: {voucher}")
        response = requests.post(rollup_server + "/voucher", json=voucher)
        logger.info(f"Received voucher status {response.status_code} body {response.content}")
    except Exception:
        logger.error("Error creating voucher.")

    return