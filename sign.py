from web3 import Web3
from abi import *

from privatekey import pk

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8000/"))
wallet = web3.toChecksumAddress("0xA3532d90A6e4C9c40ecE38019b991071c669F55B")
contract = web3.eth.contract(address=wallet, abi=sellAbi)
approve = contract.functions.approve(wallet, contract).buildTransaction({
        'from': wallet,
        'gasPrice': web3.eth.gasPrice, #web3.toWei('20', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet),
    })
txn = web3.eth.account.sign_transaction(approve, private_key=pk)
print(txn)