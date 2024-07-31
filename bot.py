import os
import json
import time
import random
import requests
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# URLs
get_url = "https://ranch-api.kuroro.com/api/Upgrades/GetPurchasableUpgrades"
buy_url = "https://ranch-api.kuroro.com/api/Upgrades/BuyUpgrade"
checkin_url = "https://ranch-api.kuroro.com/api/DailyStreak/ClaimDailyBonus"
mining_url = "https://ranch-api.kuroro.com/api/Clicks/MiningAndFeeding"
ball_url = "https://ranch-api.kuroro.com/api/EnergyBalls/TakeHitsCombo/{owner_id}:20240731"
reff_url = "https://ranch-api.kuroro.com/api/Referrals/GetReferralsState"

def read_bearer_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def create_headers(bearer_token):
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://ranch.kuroro.com',
        'Pragma': 'no-cache',
        'Referer': 'https://ranch.kuroro.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AG Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.165 Mobile',
        'Authorization': f'Bearer {bearer_token}'
    }

def perform_action(url, action_name, payload, bearer_token):
    headers = create_headers(bearer_token)
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(Fore.GREEN + f"{action_name} Success")
        else:
            print(Fore.RED + f"{action_name} - Already Tap")
    except requests.RequestException as e:
        print(Fore.RED + f"An error occurred during {action_name}: {e}")

def checkin(bearer_token):
    current_date = datetime.now().strftime("%Y-%m-%d")
    payload = {
        "date": current_date
    }
    perform_action(checkin_url, f"Check-in for {current_date}", payload, bearer_token)

def reffstate(bearer_token):
    headers = create_headers(bearer_token)
    try:
        response = requests.get(reff_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            owner_id = data.get("ownerId")
            if owner_id:
                return owner_id  
            else:
                print(Fore.RED + "Owner ID not found in response.")
                return None
        else:
            print(Fore.RED + f"Failed to retrieve referral state - Status Code: {response.status_code}")
    except requests.RequestException as e:
        print(Fore.RED + f"An error occurred during reffstate: {e}")
    return None

def update_coin(bearer_token):
    headers = create_headers(bearer_token)
    try:
        response = requests.post("https://ranch-api.kuroro.com/api/Game/UpdateCoinsSnapshot", headers=headers)
        if response.status_code == 200:
            data = response.json()
            coins_update = data.get('value')
            print(Fore.GREEN + f"[Balance] : {Fore.MAGENTA}{coins_update}{Style.RESET_ALL}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def earnrate(bearer_token):
    headers = create_headers(bearer_token)
    try:
        response = requests.get("https://ranch-api.kuroro.com/api/Game/GetPlayerState", headers=headers)
        if response.status_code == 200:
            data = response.json()
            coins_earning_rate = data.get('coinsEarningRate')
            print(Fore.GREEN + f"[Coins/Hours] : {Fore.MAGENTA}{coins_earning_rate}{Style.RESET_ALL}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def upgrade_process(bearer_token):
    headers = create_headers(bearer_token)
    response = requests.get(get_url, headers=headers)

    if response.status_code == 200:
        upgrades = response.json()
        for upgrade in upgrades:
            if upgrade['canBePurchased']:
                payload = {
                    "upgradeId": upgrade['upgradeId']
                }
                purchase_response = requests.post(buy_url, json=payload, headers=headers)
                if purchase_response.status_code == 200:
                    print(Fore.GREEN + f"Buy {upgrade['name']}")
                else:
                    print(Fore.RED + f"Not enough balance to buy {upgrade['name']} ")
    else:
        print(Fore.RED + f"Request failed with status code {response.status_code}")

def print_welcome_message():
    print(r"""
 
  _  _   _    ____  _   ___    _   
 | \| | /_\  |_  / /_\ | _ \  /_\  
 | .` |/ _ \  / / / _ \|   / / _ \ 
 |_|\_/_/ \_\/___/_/ \_\_|_\/_/ \_\
                                   

    """)
    print(Fore.GREEN + Style.BRIGHT + "KURORO RANCH BOT")
    print(Fore.CYAN + Style.BRIGHT + "Jajanin dong orang baik :)")
    print(Fore.YELLOW + Style.BRIGHT + "0x5bc0d1f74f371bee6dc18d52ff912b79703dbb54")
    print(Fore.RED + Style.BRIGHT + "Update Link: https://github.com/dcbott01/kuroro")
    print(Fore.BLUE + Style.BRIGHT + "Tukang Rename MATI AJA")

def main():
    print_welcome_message()
    user_choice = input("Do you want to proceed with upgrades for all accounts? (yes/no): ").strip().lower()

    bearer_tokens = read_bearer_tokens('query.txt')
    if not bearer_tokens:
        print(Fore.RED + "No bearer tokens found. Exiting...")
        return

    while True:
        for i, bearer_token in enumerate(bearer_tokens, start=1):
            print(Fore.BLUE + Style.BRIGHT + f"\n========== PROCESSING ACCOUNT {i} ==========")
            checkin(bearer_token)
            reffstate(bearer_token)
            update_coin(bearer_token)
            earnrate(bearer_token)
            mining_payload = {"mineAmount": 100, "feedAmount": 0}
            perform_action(mining_url, "Mining", mining_payload, bearer_token)
            feeding_payload = {"mineAmount": 0, "feedAmount": 10}
            perform_action(mining_url, "Feeding", feeding_payload, bearer_token)
            ball_payload = {"hits": 10}
            perform_action(ball_url, "Tap Ball", ball_payload, bearer_token)
            print(Fore.CYAN + Style.BRIGHT + f"\n========== PROCESSING UPGRADE ==========")
            if user_choice == 'yes':
                upgrade_process(bearer_token)
            else:
                print(Fore.YELLOW + "Skipping upgrade process for this account.")
            print(Fore.CYAN + Style.BRIGHT + f"\nFinished processing account {i}. Moving to the next account...\n")
            time.sleep(5)

        print(Fore.BLUE + Style.BRIGHT + f"\n========== SEMUA AKUN TELAH DI PROSES ==========")
        for _ in range(30):
            minutes, seconds = divmod(30 - _, 60)
            print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE])+Style.BRIGHT}==== [ Looping berikutnya {minutes} menit {seconds} detik ] ===={Style.RESET_ALL}", end="\r", flush=True)
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
