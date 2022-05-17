from web3 import Web3
from abi import abi
# import config
import time


bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
print("STATUS:", web3.isConnected())

# pancakeswap router
panRouterContractAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
# pancakeswap router abi
panabi = abi
sender_address = (input("Enter bnb  wallet address: "))  # BNB

balance = web3.eth.get_balance(sender_address)
humanReadable = web3.fromWei(balance, 'ether')

print("IN WALLET", humanReadable)
# Contract Address of Token we want to buy
amt_to_buy = float(input("Enter amount of token to buy: "))
tokenToBuy = web3.toChecksumAddress(input("Enter TokenAddress: "))  # web3.toChecksumAddress("")  # wallet address

spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  # wbnb contract address
# Setup the PancakeSwap contract
contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)
nonce = web3.eth.get_transaction_count(sender_address)
start = time.time()

# swapExactTokensForETH sell
pancakeswap2_txn = contract.functions.swapExactETHForTokens(    # swapExactTokensForTokens
    0,  # lower limit below of how much we will get
    [spend, tokenToBuy],
    sender_address,
    (int(time.time()) + 10000)  # Deadline
).buildTransaction({
    'from': sender_address,
    'value': web3.toWei(amt_to_buy, 'ether'),  # This is the Token(BNB) amount you want to Swap from
    'gas': 250000,  # Gas limit
    'gasPrice': web3.toWei('5', 'gwei'),   # Gas fees
    'nonce': nonce,
})

signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key="")  # Sign the txn
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)  # Send the txn

print("TRANS:", web3.toHex(tx_token))  # Print the txn id
