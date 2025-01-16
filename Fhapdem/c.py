import os
import time
import requests
import configparser
import datetime
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.utils import generate_mnemonic
from typing import Optional

def print_banner():
    banner = """
    ███████╗██╗  ██╗ █████╗ ██████╗ ██████╗ ███████╗███╗   ███╗
    ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝████╗ ████║
    █████╗  ███████║███████║██████╔╝██║  ██║█████╗  ██╔████╔██║
    ██╔══╝  ██╔══██║██╔══██║██╔═══╝ ██║  ██║██╔══╝  ██║╚██╔╝██║
    ██║     ██║  ██║██║  ██║██║     ██████╔╝███████╗██║ ╚═╝ ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═════╝ ╚══════╝╚═╝     ╚═╝@xghost123
    """
    print("\033[1;91m" + banner + "\033[0m")

def aggressive_message(message, color_code):
    print(f"\033[1;{color_code}m{message}\033[0m")

def show_mnemonic_animated(mnemonic):
    print("\033[93m" + "=" * 60 + "\033[0m")
    aggressive_message("🔥🔥🔥 GENERATED MNEMONIC 🔥🔥🔥", "91")
    for word in mnemonic.split():
        time.sleep(0.2)
        print(f"\033[1;92m{word}\033[0m", end=" ", flush=True)
    print("\n" + "\033[93m" + "=" * 60 + "\033[0m")

def check_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False

def mainnet_url(mainnet):
    if mainnet == "bsc":
        return "https://api.bscscan.com/"
    elif mainnet == "eth":
        return "https://api.etherscan.io/"
    elif mainnet == "polygon":
        return "https://api.polygonscan.com/"
    else:
        return "https://api.bscscan.com/"

def mainnet_api(mainnet):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['api'][mainnet]

def req_trnx(mainnet, address):
    mainnet_url_link = mainnet_url(mainnet)
    mainnet_api_key = mainnet_api(mainnet)
    module = "account"
    action = "txlist"
    page_no = 1
    display_per_page = 1
    sort = "desc"
    connection_count = 1

    while True:
        if check_connection():
            try:
                trnx_response = requests.get(
                    f"{mainnet_url_link}api?module={module}&action={action}&address={address}&page={page_no}&offset={display_per_page}&sort={sort}&apikey={mainnet_api_key}",
                    timeout=None
                )
                if trnx_response and trnx_response.status_code == 200:
                    try:
                        trnx_info = trnx_response.json()
                        if isinstance(trnx_info, dict) and "status" in trnx_info:
                            return trnx_info
                        else:
                            print("💥 Invalid transaction data received. Returning default response.")
                            return None
                    except ValueError:
                        print("💥 Failed to parse transaction data as JSON.")
                        return None
                else:
                    print(f"💥 API Request failed with status code: {trnx_response.status_code}")
                    return None
            except requests.RequestException as e:
                print(f"💥 Error during API Request: {e}")
                return None
        else:
            print(f"💥💥💥 Trying to establish a connection!!! 💥💥💥 || Checked: {connection_count} time(s) 💥💥💥\n")
            time.sleep(10)
            connection_count += 1
            os.system('cls')


def req_balance(mainnet, address):
    mainnet_url_link = mainnet_url(mainnet)
    mainnet_api_key = mainnet_api(mainnet)
    module = "account"
    action = "balance"
    connection_count = 1

    while True:
        if check_connection():
            try:
                balance_response = requests.get(
                    f"{mainnet_url_link}api?module={module}&action={action}&address={address}&apikey={mainnet_api_key}",
                    timeout=None
                )
                if balance_response and balance_response.status_code == 200:
                    try:
                        balance_info = balance_response.json()
                        if isinstance(balance_info, dict) and "status" in balance_info:
                            return balance_info
                        else:
                            print("💥 Invalid balance data received. Returning default response.")
                            return None
                    except ValueError:
                        print("💥 Failed to parse balance data as JSON.")
                        return None
                else:
                    print(f"💥 API Request failed with status code: {balance_response.status_code}")
                    return None
            except requests.RequestException as e:
                print(f"💥 Error during API Request: {e}")
                return None
        else:
            print(f"💥💥💥 Trying to establish a connection!!! 💥💥💥 || Checked: {connection_count} time(s) 💥💥💥\n")
            time.sleep(10)
            connection_count += 1
            os.system('cls')


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()

    check_mainnet = ['bsc', 'eth', 'polygon']

    hasTransactionPath = "hasTransaction"
    hasBalancePath = "hasBalance"

    todays_date = datetime.date.today()

    looper_count = 0
    balanceFound_count = 0
    trnxFound_count = 0
    init_run_time = time.monotonic()
    run_time = 0
    execution_time = 0
    looper = True
    while looper:
        start_time = time.monotonic()

        print(f"💥💥💥 Total Checked: {looper_count} || Execution Time: {execution_time} || Elapsed Time: {run_time} 💥 💥💥")
        print(f"🔥🔥🔥 Transactions Found: {trnxFound_count} || Balances Found: {balanceFound_count} 🔥🔥🔥")

        MNEMONIC = generate_mnemonic(language="english", strength=128)
        show_mnemonic_animated(MNEMONIC)

        bip44_hdwallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
        bip44_hdwallet.from_mnemonic(mnemonic=MNEMONIC, language="english", passphrase=None)

        aggressive_message(f"⚡⚡⚡ Wallet Address: {bip44_hdwallet.address()} ⚡⚡⚡", "92")

        for mainnet in check_mainnet:
            wallet_trnx_status = req_trnx(mainnet, bip44_hdwallet.address())
            aggressive_message(f"🔥🔥🔥 Checking Transactions on {mainnet} 🔥🔥🔥", "91")
            if wallet_trnx_status and wallet_trnx_status.get("status") == "1":
                trnxFound_count += 1
                aggressive_message(f"💥💥💥 FOUND TRANSACTION on {mainnet} 💥💥💥", "92")
                with open(r"{}\hasTransaction-{}.txt".format(hasTransactionPath, todays_date), "a") as hb:
                    hb.write(mainnet)
                    hb.write(" - ")
                    hb.write(" || Mnemonic : ")
                    hb.write(bip44_hdwallet.mnemonic())
                    hb.write(" || ")
                    hb.write(bip44_hdwallet.address())
                    hb.write(" ")
                    hb.write('\n')
                aggressive_message(f"🔥🔥🔥 Checking Balance on {mainnet} 🔥🔥🔥", "91")
                wallet_trnx_balance = req_balance(mainnet, bip44_hdwallet.address())
                if wallet_trnx_balance and wallet_trnx_balance.get["result"] != "0":
                    balanceFound_count += 1
                    aggressive_message(f"💥💥💥 FOUND BALANCE on {mainnet} 💥💥💥", "92")
                    with open(r"{}\hasBalance-{}.txt".format(hasBalancePath, todays_date), "a") as hb:
                        hb.write(mainnet)
                        hb.write(" - ")
                        hb.write(wallet_trnx_balance["result"])
                        hb.write(" || Mnemonic : ")
                        hb.write(bip44_hdwallet.mnemonic())
                        hb.write(" || ")
                        hb.write(bip44_hdwallet.address())
                        hb.write(" ")
                        hb.write('\n')
                else:
                    aggressive_message(f"💥💥💥 No Balance Found on {mainnet} 💥💥💥", "91")
            else:
                aggressive_message(f"💥💥💥 No Transaction Found on {mainnet} 💥💥💥", "91")

        looper_count += 1
        end_time = time.monotonic()
        execution_time = datetime.timedelta(seconds=end_time - start_time)
        run_time = datetime.timedelta(seconds=end_time - init_run_time)
        bip44_hdwallet.clean_derivation()
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()

if __name__ == '__main__':
    main()