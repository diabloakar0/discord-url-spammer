import requests
import time
import random
import threading
import os
from colorama import Fore, Style, init
from datetime import datetime

os.system('cls')
init(autoreset=True)

vanity = "spamtestxd"
server_id = "1253494877304651787"
webhook_url = "https://discord.com/api/webhooks/1254143910134157312/E-_eiQy8GkS41QrqWe7VFmTYNTr-uR33R-2YUp6VcnIoM-6jPs6tX6t0WXWHik2iqfBS"
banli = True
request_delay = 0.008

user_tokens = []

def load_user_tokens_from_file(filename):
    with open(filename, "r") as file:
        for line in file:
            user_tokens.append(line.strip())

def get_current_time():
    return datetime.now().strftime('%H:%M:%S')

def log_message(message, token, response_value, color=Fore.LIGHTBLUE_EX):
    print(f"{Fore.YELLOW}[{get_current_time()}] {color}{message} {Fore.RED}[{Fore.CYAN}{token}{Fore.RED}] {Style.RESET_ALL}[{Fore.WHITE}coded by. wia$e & diabloakar ({response_value}){Style.RESET_ALL}]")

def find_with_retry():
    retry_time = 1.4 + 0.2
    log_message(f"Retry time: {retry_time:.2f}", "N/A", "N/A", Fore.GREEN)
    attempt = 0
    loop = True

    while loop:
        time.sleep(request_delay)
        attempt += 1
        try:
            user_cookie = random.choice(user_tokens)
            headers = {"Content-Type": "application/json", "Authorization": user_cookie}
            response = requests.get(f"https://discord.com/api/v9/invites/{vanity}", headers=headers)

            if response.status_code == 404:
                if banli:
                    time.sleep(0.5)
                    log_message("Kapılıyor..", user_cookie, response.status_code, Fore.LIGHTWHITE_EX)
                    keep(user_cookie)
                    response = requests.get(f"https://discord.com/api/v9/invites/{vanity}", headers=headers)
                    if response.status_code == 200:
                        log_message("Kapıldı", user_cookie, response.status_code, Fore.GREEN)
                        send_webhook_message(f"@everyone saskin sana ne dedim {vanity}", "https://cdn.discordapp.com/attachments/1001899874922537010/1254458322283921510/indir_2.gif")
                        loop = False
                else:
                    log_message("Kapılıyor..", user_cookie, response.status_code, Fore.LIGHTWHITE_EX)
                    keep(user_cookie)
                    send_webhook_message(f"@everyone saskin sana ne dedim {vanity}", "https://cdn.discordapp.com/attachments/1001899874922537010/1254458322283921510/indir_2.gif")
                    loop = False

            elif response.status_code == 429:
                log_message("[HATA] Rate limited. Trying with another token...", user_cookie, response.status_code, Fore.RED)

            else:
                for i in range(15):
                    log_message(f"URL in use. Retrying {attempt}", user_cookie, response.status_code, Fore.LIGHTBLUE_EX)

        except requests.exceptions.RequestException as e:
            error_message = str(e)
            log_message(f"Error occurred: {error_message}", "N/A", "RequestException", Fore.RED)
            send_webhook_message(f"Error checking URL: {error_message}", "https://cdn.discordapp.com/attachments/1001899874922537010/1254458322283921510/indir_2.gif")

def keep(user_cookie):
    payload = {"code": vanity}
    headers = {"Content-Type": "application/json", "Authorization": user_cookie}
    try:
        response = requests.patch(f"https://discord.com/api/v9/guilds/{server_id}/vanity-url", json=payload, headers=headers)
        log_message(response.text, user_cookie, response.status_code, Fore.GREEN)
    except requests.exceptions.RequestException as e:
        error_message = str(e)
        log_message(f"Error occurred: {error_message}", user_cookie, "RequestException", Fore.RED)
        send_webhook_message(f"Error updating vanity URL: {error_message}", "https://cdn.discordapp.com/attachments/1001899874922537010/1254458322283921510/indir_2.gif")

def checkToken(user_cookie):
    headers = {"Content-Type": "application/json", "Authorization": user_cookie}
    while True:
        time.sleep(10)
        try:
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
            if response.status_code == 200:
                log_message("Token valid", user_cookie, response.status_code, Fore.GREEN)
            else:
                log_message("Token invalid", user_cookie, response.status_code, Fore.RED)
                send_webhook_message("Invalid token", "https://cdn.discordapp.com/attachments/1001899874922537010/1254458322283921510/indir_2.gif")
        except requests.exceptions.RequestException as e:
            error_message = str(e)
            log_message(f"Error occurred: {error_message}", user_cookie, "RequestException", Fore.RED)
            send_webhook_message(f"Error checking token: {error_message}", "https://cdn.discordapp.com/attachments/1001899874922537010/1254458322283921510/indir_2.gif")

def send_webhook_message(message, image_url=None):
    data = {"content": message}
    if image_url:
        data["embeds"] = [{"image": {"url": image_url}}]
    try:
        requests.post(webhook_url, json=data)
    except requests.exceptions.RequestException as e:
        error_message = str(e)
        log_message(f"Error occurred: {error_message}", "N/A", "RequestException", Fore.RED)

if __name__ == "__main__":
    load_user_tokens_from_file("tokens.txt")

    threads = []
    num_threads = 1

    for _ in range(num_threads):
        t = threading.Thread(target=find_with_retry)
        t.start()
        threads.append(t)

    valid_token = user_tokens[0] if user_tokens else None
    t2 = threading.Thread(target=checkToken, args=(valid_token,))
    t2.start()
    threads.append(t2)

    for t in threads:
        t.join()
