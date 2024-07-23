import requests
import time
from colorama import Fore, Style, init
from datetime import datetime
import json
import random

# Initialize colorama
init(autoreset=True)

# URLs
get_url = "https://ranch-api.kuroro.com/api/Upgrades/GetPurchasableUpgrades"
buy_url = "https://ranch-api.kuroro.com/api/Upgrades/BuyUpgrade"
checkin_url = "https://ranch-api.kuroro.com/api/DailyStreak/ClaimDailyBonus"
mining_url = "https://ranch-api.kuroro.com/api/Clicks/MiningAndFeeding"

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
            print(Fore.GREEN + f"Successfully performed {action_name}")
        else:
            print(Fore.RED + f"Failed to perform {action_name} - Udah Abis Jir")
    except requests.RequestException as e:
        print(Fore.RED + f"An error occurred during {action_name}: {e}")

def checkin(bearer_token):
    current_date = datetime.now().strftime("%Y-%m-%d")
    payload = {
        "date": current_date
    }
    perform_action(checkin_url, f"Check-in for {current_date}", payload, bearer_token)

def upgrade_process(bearer_token):
    headers = create_headers(bearer_token)
    response = requests.get(get_url, headers=headers)

    if response.status_code == 200:
        upgrades = response.json()

        # Step 4: Purchase an upgrade
        for upgrade in upgrades:
            if upgrade['canBePurchased']:
                payload = {
                    "upgradeId": upgrade['upgradeId']
                }
                purchase_response = requests.post(buy_url, json=payload, headers=headers)
                if purchase_response.status_code == 200:
                    print(Fore.GREEN + f"Successfully purchased upgrade: {upgrade['name']}")
                else:
                    print(Fore.RED + f"Failed to purchase upgrade: {upgrade['name']} - Duit lu Ga cukup bre $$$")
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

def process_accounts(user_choice):
    bearer_tokens = read_bearer_tokens('query.txt')
    
    for i, bearer_token in enumerate(bearer_tokens, start=1):
        print(Fore.BLUE + Style.BRIGHT + f"\n========== PROCESSING ACCOUNT {i} ==========")
        
        # Step 1: Check-in for the daily bonus
        checkin(bearer_token)
        
        # Step 2: Perform Mining and Feeding
        mining_payload = {"mineAmount": 100, "feedAmount": 0}
        perform_action(mining_url, "Mining", mining_payload, bearer_token)
        
        feeding_payload = {"mineAmount": 0, "feedAmount": 1000}
        perform_action(mining_url, "Feeding", feeding_payload, bearer_token)

        # Perform upgrade process based on user choice
        if user_choice == 'yes':
            upgrade_process(bearer_token)
        else:
            print(Fore.YELLOW + "Skipping upgrade process for this account.")
        
        # Print message indicating transition to the next account
        print(Fore.CYAN + Style.BRIGHT + f"\nFinished processing account {i}. Moving to the next account...\n")
        time.sleep(5)
    
    # Print completion message and start countdown
    print(Fore.BLUE + Style.BRIGHT + f"\n========== SEMUA AKUN TELAH DI PROSES ==========")
    for _ in range(1800):
        minutes, seconds = divmod(1800 - _, 60)
        print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE])+Style.BRIGHT}==== [ Looping berikutnya {minutes} menit {seconds} detik ] ===={Style.RESET_ALL}", end="\r", flush=True)
        time.sleep(1)

def main():
    print_welcome_message()  # Print the welcome message at the start
    
    # Ask user if they want to proceed with upgrades
    user_choice = input("Do you want to proceed with upgrades for all accounts? (yes/no): ").strip().lower()
    
    while True:
        process_accounts(user_choice)  # Process all accounts
        # You can add logic here if you need to break the loop or handle interruptions

if __name__ == "__main__":
    main()
