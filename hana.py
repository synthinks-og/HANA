from web3 import Web3
import json
import time
from colorama import init, Fore, Style

init(autoreset=True)

print(Fore.CYAN + Style.BRIGHT + """ █████╗ ██████╗ ███████╗███╗   ███╗██╗██████╗ ███╗   ██╗""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """██╔══██╗██╔══██╗██╔════╝████╗ ████║██║██╔══██╗████╗  ██║""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """███████║██║  ██║█████╗  ██╔████╔██║██║██║  ██║██╔██╗ ██║""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """██╔══██║██║  ██║██╔══╝  ██║╚██╔╝██║██║██║  ██║██║╚██╗██║""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """██║  ██║██████╔╝██║     ██║ ╚═╝ ██║██║██████╔╝██║ ╚████║""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝     ╚═╝╚═╝╚═════╝ ╚═╝  ╚═══╝""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """t.me/dpangestuw31""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """Auto Deposit ETH for HANA Network""" + Style.RESET_ALL)

# Konfigurasi
RPC_URL = "https://mainnet.base.org"
CONTRACT_ADDRESS = "0xC5bf05cD32a14BFfb705Fb37a9d218895187376c"
AMOUNT_ETH = 0.000000000000000001  # Jumlah ETH yang akan didepositkan

web3 = Web3(Web3.HTTPProvider(RPC_URL))

num_transactions = int(input(Fore.YELLOW + "Masukkan jumlah transaksi yang ingin dilakukan: " + Style.RESET_ALL))

with open("pvkey.txt", "r") as file:
    private_keys = [line.strip() for line in file if line.strip()]

contract_abi = '''
[
    {
        "constant": false,
        "inputs": [],
        "name": "depositETH",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]
'''

amount_wei = web3.to_wei(AMOUNT_ETH, 'ether')
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=json.loads(contract_abi))

for i in range(num_transactions):
    for private_key in private_keys:
        from_address = web3.eth.account.from_key(private_key).address
        short_from_address = from_address[:4] + "..." + from_address[-4:]

        transaction = contract.functions.depositETH().build_transaction({
            'from': from_address,
            'value': amount_wei,
            'gas': 100000,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(from_address),
        })

        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(Fore.GREEN + f"Transaksi ke-{i + 1} berhasil dikirim dari {short_from_address} dengan hash: {tx_hash.hex()}")

        time.sleep(3)

print(Fore.MAGENTA + "Selesai melakukan transaksi.")
