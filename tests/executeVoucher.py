from web3 import Web3
import json
import time
import rsa

anvil = "http://localhost:8545"
web3 = Web3(Web3.HTTPProvider(anvil))

def str2hex(str):
    return "0x" + str.encode("utf-8").hex()

cartesiDapp_address = "0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e"
cartesiDapp_checksum_address = Web3.to_checksum_address(cartesiDapp_address)
with open("./front-end/abi-contracts/CartesiDApp.json", "r") as abi:
    cartesiDapp_ABI = json.load(abi)
cartesiDapp_contract = web3.eth.contract(abi=cartesiDapp_ABI, address=cartesiDapp_checksum_address)

wallet_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
# dapp_address = "0xab7528bb862fB57E8A2BCd567a2e929a0Be56a5e"

destination = "0x59b670e9fA9D0A427751Af201D676719a970857b"
payload = "0x7472616e73666572283078663339666436653531616164383866366634636536616238383237323739636666666239323236362c20313029"
payload = Web3.to_bytes(hexstr=payload)
proof = {}

gas = web3.eth.gas_price
nonce = web3.eth.get_transaction_count(wallet_address)
tx = cartesiDapp_contract.functions.executeVoucher(destination, payload, proof).build_transaction({'from':wallet_address, 'nonce':nonce, 'gasPrice': gas})
signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction).hex()

print(tx_hash)