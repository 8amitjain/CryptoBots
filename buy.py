from web3 import Web3
from abi import abi
import time
from privatekey import pk

#0x8BaBbB98678facC7342735486C851ABD7A0d17Ca # ETH

bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
web3 = Web3(Web3.HTTPProvider(bsc))
print("STATUS:", web3.isConnected())

# pancakeswap router
panRouterContractAddress = web3.toChecksumAddress('0x9ac64cc6e4415144c455bd8e4837fea55603e5c3')  # 0x10ED43C718714eb63d5aA57B78B54704E256024E
# pancakeswap router abi
panabi = abi
sender_address = "0xA3532d90A6e4C9c40ecE38019b991071c669F55B"  #(input("Enter bnb  wallet address: "))  # BNB

balance = web3.eth.get_balance(sender_address)
print(balance)
humanReadable = web3.fromWei(balance, 'ether')

print("IN WALLET", humanReadable)
# Contract Address of Token we want to buy
# amt_to_buy = float(input("Enter amount of token to buy: "))
tokenToBuy = web3.toChecksumAddress("0x7ef95a0FEE0Dd31b22626fA2e10Ee6A223F8a684")  # wallet address
    # web3.toChecksumAddress(input("Enter TokenAddress: "))  #
spend = web3.toChecksumAddress("0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd")  # wbnb contract address 0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c
# Setup the PancakeSwap contract

contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)

nonce = web3.eth.get_transaction_count(sender_address)
start = time.time()

# swapExactTokensForETH sell swapExactETHForTokens
pancakeswap2_txn = contract.functions.swapExactETHForTokens(    # swapExactTokensForTokens
    0,  # lower limit below of how much we will getd
    [spend, tokenToBuy],
    sender_address,
    (int(time.time()) + 10000)  # Deadline
).buildTransaction({
    'from': sender_address,
    'value': web3.toWei(0.01, 'ether'),  # This is the Token(BNB) amount you want to Swap from
    'gas': 250000,  # Gas limit
    'gasPrice': web3.toWei('10', 'gwei'),   # Gas fees
    'nonce': nonce,
})


signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=pk)  # Sign the txn
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)  # Send the txn

print("TRANS:", web3.toHex(tx_token))  # Print the txn idpb
print("TRANS:",tx_token)  # Print the txn idpb