from web3 import Web3
from abi import *
import time
from privatekey import pk
TEST = True

bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/" if TEST else "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
print("STATUS:", web3.isConnected())
# TRY CATCH

panRouterContractAddress = web3.toChecksumAddress("0x9ac64cc6e4415144c455bd8e4837fea55603e5c3") if TEST else '0x10ED43C718714eb63d5aA57B78B54704E256024E'

wallet = web3.toChecksumAddress("0xA3532d90A6e4C9c40ecE38019b991071c669F55B")
tokenA = web3.toChecksumAddress("0x7ef95a0FEE0Dd31b22626fA2e10Ee6A223F8a684")  # USDT
tokenB = web3.toChecksumAddress("0x8BaBbB98678facC7342735486C851ABD7A0d17Ca")  # ETH
wbnb_contract = web3.toChecksumAddress("0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd")  # BNB

amt = 5   # in BNB

# GET bal and try catchb

# token = web3.eth.contract(address=tokenA, abi=sellAbi)
# balance = token.functions.balanceOf({tokenA}).call()
# humanReadable = web3.fromWei(balance, 'ether')
# print("IN WALLET USDT", humanReadable)
#
# balance = web3.eth.get_balance(tokenB)
# humanReadable = web3.fromWei(balance, 'ether')
# print("IN WALLET ETH", humanReadable)


balance = web3.eth.get_balance(wallet)
humanReadable = web3.fromWei(balance, 'ether')
print("IN WALLET", humanReadable)

contract = web3.eth.contract(address=panRouterContractAddress, abi=abi)
nonce = web3.eth.get_transaction_count(wallet)
# start = time.time()


def bnb_buy():
    pancakeswap2 = contract.functions.swapExactETHForTokens(  # swapExactTokensForTokens
        0,  # lower limit below of how much we will getd
        [wbnb_contract, tokenA],
        wallet,
        (int(time.time()) + 10000)  # Deadline
    ).buildTransaction({
        'from': wallet,
        'value': web3.toWei(amt, 'ether'),  # This is the Token(BNB) amount you want to Swap from
        'gas': 250000,  # Gas limit
        'gasPrice': web3.toWei('10', 'gwei'),  # Gas fees
        'nonce': nonce,
    })

    return pancakeswap2


def bnb_sell():
    sell_token = web3.eth.contract(tokenA, abi=sellAbi)
    bal = sell_token.functions.balanceOf(wallet).call()
    symbol = sell_token.functions.symbol().call()
    readable = web3.fromWei(bal, 'ether')
    print("Balance: " + str(readable) + " " + symbol)
    approve = sell_token.functions.approve(panRouterContractAddress, balance).buildTransaction({
        'from': wallet,
        'gasPrice': web3.toWei('10', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet),
    })
    txn = web3.eth.account.sign_transaction(approve, private_key=pk)
    tran_tk = web3.eth.send_raw_transaction(txn.rawTransaction)
    print("Approved: " + web3.toHex(tran_tk))

    time.sleep(15)

    pancakeswap2 = contract.functions.swapExactTokensForETH(
        web3.toWei(amt, 'ether'), 0,
        [tokenA, wbnb_contract],
        wallet,
        (int(time.time()) + 1000000)

    ).buildTransaction({
        'from': wallet,
        'gas': 250000,  # Gas limit
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet),
    })

    return pancakeswap2


def token_to_token_swap():
    sell_token = web3.eth.contract(tokenA, abi=sellAbi)
    approve = sell_token.functions.approve(panRouterContractAddress, balance).buildTransaction({
        'from': wallet,
        'gasPrice': web3.toWei('10', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet),
    })
    txn = web3.eth.account.sign_transaction(approve, private_key=pk)
    tran_tk = web3.eth.send_raw_transaction(txn.rawTransaction)
    print("Approved: " + web3.toHex(tran_tk))

    time.sleep(10)

    pancakeswap2 = contract.functions.swapExactTokensForTokens(
        web3.toWei(amt, 'ether'), 0,
        [tokenA, tokenB],  # USD
        wallet,  # ETH
        (int(time.time()) + 1000000)
    ).buildTransaction({
        'from': wallet,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet),
    })

    return pancakeswap2


def add_liquidity():
    token_contrack = web3.eth.contract(tokenA, abi=sellAbi)
    total_supply = token_contrack.functions.totalSupply().call()
    print(web3.fromWei(total_supply, 'ether'))

    approve = token_contrack.functions.approve(panRouterContractAddress, total_supply).buildTransaction({
        'from': wallet,
        'gasPrice': web3.eth.gasPrice, #web3.toWei('10', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet),
    })
    txn = web3.eth.account.sign_transaction(approve, private_key=pk)
    tran_tk = web3.eth.send_raw_transaction(txn.rawTransaction)
    print("Approved: " + web3.toHex(tran_tk))

    token_contrack = web3.eth.contract(tokenB, abi=sellAbi)
    total_supply = token_contrack.functions.totalSupply().call()

    # print(web3.fromWei(total_supply, 'ether'))
    # amt = contract.functions.quote(1, total_supply_1, total_supply).call()
    # print(amt)

    approve = token_contrack.functions.approve(panRouterContractAddress, total_supply).buildTransaction({
        'from': wallet,
        'gasPrice': web3.eth.gasPrice, #web3.toWei('20', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet),
    })
    txn = web3.eth.account.sign_transaction(approve, private_key=pk)
    tran_tk = web3.eth.send_raw_transaction(txn.rawTransaction)
    print("Approved: " + web3.toHex(tran_tk))
    time.sleep(10)
    pancakeswap2 = contract.functions.addLiquidity(
        tokenA, tokenB,
        web3.toWei(1, 'ether'), web3.toWei(0.000558655, 'ether'),
        0, 0,
        wallet,  # ETH
        (int(time.time()) + 1000000)
    ).buildTransaction({
        'from': wallet,
        'gasPrice': web3.eth.gasPrice, #web3.toWei('20', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet),
    })

    return pancakeswap2

# pancakeswap2_txn = bnb_buy()
pancakeswap2_txn = bnb_sell()
# pancakeswap2_txn = token_to_token_swap()
# pancakeswap2_txn = add_liquidity()

signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=pk)  # Sign the txn
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)  # Send the txn

print("TRANS:", web3.toHex(tx_token))  # Print the txn hash
