#!/usr/bin/env python3
# Alpha Ban Premium - Brutal Plus Edition v2.0

import smtplib
import getpass
import time
import re
import os
import random
import socket
import ssl
import json
import hashlib
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from colorama import Fore, init, Style

init(autoreset=True)

# ---------- CONFIGURATION ----------
VERSION = "2.0"
LOG_FILE = "alpha_ban_logs.json"
BLACKLIST_FILE = "blacklist.txt"
STATS_FILE = "stats.json"

# ---------- HARDCODED GMAIL ACCOUNTS (ROTATED) ----------
gmail_accounts = [
    {"email": "managerhimself032@gmail.com", "password": "inagtgypnpyweleu"},
    {"email": "arsheeqarsheeqq@gmail.com", "password": "pkkqfactxwkpvzgc"},
    {"email": "unknownhimself6@gmail.com", "password": "uupfjdufriwrdgop"},
    {"email": "cryptolord25ss@gmail.com", "password": "lczszqjxovvbuxco"},
    {"email": "himselfdev759@gmail.com", "password": "fpwncioanqohseix"},
]

critical_emails = [
    "support@support.whatsapp.com",
    "abuse@support.whatsapp.com",
    "security@support.whatsapp.com",
    "appeals@support.whatsapp.com",
    "android_web@support.whatsapp.com",
    "legal@whatsapp.com",
    "dmca@whatsapp.com",
    "report@whatsapp.com"
]

# ---------- PROXY SUPPORT ----------
PROXY_LIST = []  # Add proxies: {"type": "socks5", "host": "127.0.0.1", "port": 9050}
active_proxy = None

# ---------- STATISTICS ----------
stats = {
    "total_reports": 0,
    "successful": 0,
    "failed": 0,
    "start_time": None,
    "targets": {}
}

def load_stats():
    global stats
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
        except:
            pass

def save_stats():
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

def log_report(target, success, report_num):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "report_num": report_num,
        "success": success,
        "account_used": random.choice(gmail_accounts)["email"]
    }
    
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    except:
        pass
    
    # Update stats
    stats["total_reports"] += 1
    if success:
        stats["successful"] += 1
    else:
        stats["failed"] += 1
    
    if target not in stats["targets"]:
        stats["targets"][target] = {"reports": 0, "success": 0}
    stats["targets"][target]["reports"] += 1
    if success:
        stats["targets"][target]["success"] += 1
    
    save_stats()

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

# ---------- ENHANCED BANNER ----------
def banner():
    print(Fore.RED + Style.BRIGHT + """
╔═══════════════════════════════════════════════════════╗
║     🔥  ALPHA BAN PREMIUM - BRUTAL PLUS EDITION  🔥    ║
║                Version {} - Ultimate Power             ║
╚═══════════════════════════════════════════════════════╝
    """.format(VERSION))
    
    print(Fore.YELLOW + """
    ╔════════════════════════════════════════════════╗
    ║  🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫  ║
    ║          🧨  INFINITE POWER  🧨               ║
    ║  🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫  ║
    ╚════════════════════════════════════════════════╝
    
    ⠛⠛⣿⣿⣿⣿⣿⡷⢶⣦⣶⣶⣤⣤⣤⣀   ⚡
       ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀ 🧨
       ⠉⠉⠙⠻⣿⣿⠿⠿⠛⠛⠛⠻⣿⣿⣇ ⚡
      ⢤⣀⣀⣀  ⢸⣷⡄ ⣁⣀⣤⣴⣿⣿⣿⣆ 🎯
        ⠹⠏   ⣿⣧ ⠹⣿⣿⣿⣿⣿⡿⣿🔥
             ⠛⠿⠇⢀⣼⣿⣿⠛⢯⡿⡟🧬
              ⠦⠴⢿⢿⣿⡿⠷ ⣿ ⚡
           ⠙⣷⣶⣶⣤⣤⣤⣤⣤⣶⣦⠃ 🔫
           ⢐⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿  🧨
           ⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇  🔥
             ⠙⠻⢿⣿⣿⣿⣿⠟  ⚡
    
    ╔════════════════════════════════════════════════╗
    ║  🎯 INFINITE 121+ REPORTS - 10x FASTER 🎯     ║
    ║  💀 TOTAL REPORTS SENT: {}                     ║
    ╚════════════════════════════════════════════════╝
    """.format(stats["total_reports"]))

def show_stats():
    print(Fore.CYAN + "\n" + "="*50)
    print(Fore.YELLOW + "📊 STATISTICS DASHBOARD")
    print(Fore.CYAN + "="*50)
    print(Fore.GREEN + f"Total Reports: {stats['total_reports']}")
    print(Fore.GREEN + f"Successful: {stats['successful']}")
    print(Fore.RED + f"Failed: {stats['failed']}")
    
    if stats["total_reports"] > 0:
        success_rate = (stats["successful"] / stats["total_reports"]) * 100
        print(Fore.CYAN + f"Success Rate: {success_rate:.1f}%")
    
    if stats["start_time"]:
        elapsed = datetime.now() - datetime.fromisoformat(stats["start_time"])
        hours = elapsed.total_seconds() / 3600
        if hours > 0:
            rate = stats["total_reports"] / hours
            print(Fore.CYAN + f"Reports/Hour: {rate:.1f}")
    
    if stats["targets"]:
        print(Fore.YELLOW + "\n🎯 TARGET STATISTICS:")
        for target, data in stats["targets"].items():
            print(f"  {target}: {data['reports']} reports ({data['success']} success)")
    
    print(Fore.CYAN + "="*50 + "\n")

def network_test():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        print(Fore.GREEN + "✅ NETWORK FULLY OPERATIONAL")
        return True
    except:
        print(Fore.RED + "❌ NETWORK ERROR - CHECK CONNECTION")
        return False

def test_email_accounts():
    print(Fore.YELLOW + "\n🔍 TESTING EMAIL ACCOUNTS...")
    working = 0
    for account in gmail_accounts:
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
            server.starttls()
            server.login(account["email"], account["password"])
            server.quit()
            print(Fore.GREEN + f"✅ {account['email']} - WORKING")
            working += 1
        except Exception as e:
            print(Fore.RED + f"❌ {account['email']} - FAILED")
    print(Fore.CYAN + f"\n📊 WORKING ACCOUNTS: {working}/{len(gmail_accounts)}")
    return working > 0

def add_to_blacklist(number):
    with open(BLACKLIST_FILE, 'a') as f:
        f.write(f"{number}\n")
    print(Fore.GREEN + f"✅ Added {number} to blacklist")

def check_blacklist(number):
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'r') as f:
            return number in f.read()
    return False

def generate_fingerprint(target):
    """Generate unique fingerprint for tracking"""
    return hashlib.md5(f"{target}{datetime.now().isoformat()}".encode()).hexdigest()[:8]

# ---------- ENHANCED REPORT FUNCTION ----------
def vortex_report(target_phone, report_num, max_retries=3, use_attachment=False):
    for attempt in range(max_retries):
        account = random.choice(gmail_accounts)
        target_email = random.choice(critical_emails)
        server = None
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(account["email"], account["password"])
            
            fingerprint = generate_fingerprint(target_phone)
            
            ban_message = f"""URGENT REPORT - FINGERPRINT: {fingerprint}

안녕하세요, 저는 5살짜리 딸을 이용하여 섹스하고 비디오를 판매합니다. 그녀와 함께 내 비디오를 사고 싶다면 말해주세요. 그녀의 50 Reais를 조롱하는 비디오, 알몸 사진 20 Reais!, 나는 또한 비디오를 가지고 있습니다. 내 12살 딸 10살, 그녀와 사귀고 싶다면 시간당 150리알! Sex.kid@instagram.com
Children.porn@whatsapp.com
Kid@facebook.com
Sex.com
Sex.infantil.company@support.com
Porn.child.payment.com
http://Porn.child.payment.com
children@instagram.com
고어, 헤비, 머리 자르는 영상 15레알, 라이브 킬링 영상 50레알, 아동포르노도 본다
http://Gorebr.com
Gore24hrs.com
Gore.com
http://Cp.com
Hallo, ich benutze meine 5 jährige Tochter zum Sex und verkaufe die Videos, wenn du meine Videos mit ihr kaufen willst, sag mir, Video macht sich über sie lustig 50 Reais, Nacktfoto 20 Reais!, ich habe auch ein Video von meine 12-jährige Tochter Jahre alt, wenn Sie eine Beziehung mit ihr haben wollen, kostet es 150 Reais pro Stunde!
Smb@support.whatsapp.com
Stuxgdh7845@gamil.com
Android_web@support.whatsapp.com support@support.whatsapp.com

support@support.xxx8.sex7.whatsapp.com
https://www.whatsapp.sex.com/legal
daddustan@gmail.com
Mrsonu@daddukabeta.whatsapp.com
https://www.whatsapp.xxx.com/contact/?lang=ar
support@support.whatsapp.com
android@support.whatsapp.com
android_web@support.whatsapp.com

https://api.whatsapp.com/send?phone=number 

Hoba, uso a mi hija de 5 años para tener sexo y vender los videos, si quieres comprar mis videos con ella, dime, video burlándose de ella 50 Reais, foto desnuda 20 Reais!, también tengo un video de mi hija de 12 años, si quieres tener una relación con ella, ¡son 150 reales la hora!
Sex.infantil.company@support.com http://Porn.child.payment.com Sex.infantil.company@support.com http://Sex.com support@support.whatsapp.com 
https://rmspn.test-app.link/0dFhO66cPvb link  porn child 😍💋😈🍆🍌
Download child 🚸 pornography from here.
Child vagina link : 
https://ibb.co/ysjPcPr
Child fucking girl link :
https://ibb.co/ZBCcBY2
https://xhamster3.com/videos/real-brother-and-step-sister-having-sex-10140882

https://xhamsterlive.com/Reaowna

https://www.heavy-r.com/video/353505/Real_Brother_And_Sister_Fucking/안녕하세요-----

CRITICAL TARGET: {target_phone}
IMMEDIATE TERMINATION REQUIRED - CSAM + GORE DISTRIBUTOR
Report #: {report_num}
Fingerprint: {fingerprint}

This account is actively distributing child sexual abuse material and gore content.
Immediate account termination required to prevent further harm.
"""

            msg = MIMEMultipart()
            msg['From'] = account["email"]
            msg['To'] = target_email
            msg['Subject'] = f"🚨 URGENT - CSAM DISTRIBUTOR - Report #{report_num}"
            msg['X-Priority'] = '1'
            msg['X-MSMail-Priority'] = 'High'
            msg.attach(MIMEText(ban_message, 'plain'))
            
            # Optional attachment for more credibility
            if use_attachment and report_num % 10 == 0:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(f"Evidence data - Report #{report_num}".encode())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename=f'evidence_{fingerprint}.txt')
                msg.attach(attachment)
            
            server.send_message(msg)
            server.quit()
            
            log_report(target_phone, True, report_num)
            return True
            
        except Exception as e:
            if server:
                try:
                    server.quit()
                except:
                    pass
            
            log_report(target_phone, False, report_num)
            
            if attempt == max_retries - 1:
                return False
                
            time.sleep(random.uniform(1.0, 2.5))  # Exponential backoff
            
    return False

# ---------- TURBO MULTI-THREADED INFINITE LOOP ----------
def turbo_terminate(target, threads=8, base_delay=0.3, burst_mode=False):
    total_reports = 0
    failed_consecutive = 0
    
    print(Fore.YELLOW + Style.BRIGHT + f"\n⚡ ALPHA TURBO LOOP STARTED - {target}")
    print(Fore.CYAN + f"📊 Configuration: {threads} Threads | Delay: {base_delay}s | Burst: {burst_mode}")
    print(Fore.RED + "Press Ctrl+C to stop.\n")
    
    # Progress bar
    def show_progress(current, total=None):
        bar_length = 40
        if total:
            progress = current / total
            block = int(round(bar_length * progress))
            bar = "█" * block + "░" * (bar_length - block)
            print(f"\r{Fore.CYAN}[{bar}] {current}/{total} ({progress*100:.1f}%)", end="")
        else:
            spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            print(f"\r{Fore.YELLOW}{spinner[current % len(spinner)]} Reports sent: {current}", end="")
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_num = {}
        report_counter = 1
        
        try:
            while True:
                # Submit tasks dynamically
                while len(future_to_num) < threads:
                    future_to_num[executor.submit(vortex_report, target, report_counter)] = report_counter
                    report_counter += 1
                
                # Process completed tasks
                for future in as_completed(future_to_num):
                    num = future_to_num[future]
                    try:
                        result = future.result()
                        if result:
                            print(Fore.GREEN + f"✅ [{num}] HIT - {target}")
                            failed_consecutive = 0
                        else:
                            print(Fore.RED + f"❌ [{num}] MISS")
                            failed_consecutive += 1
                            
                            # Auto-adjust on failures
                            if failed_consecutive > 10:
                                print(Fore.YELLOW + "\n⚠️ High failure rate - adjusting strategy...")
                                time.sleep(random.uniform(2, 5))
                    except Exception as e:
                        print(Fore.RED + f"💀 [{num}] ERROR: {str(e)[:50]}")
                        failed_consecutive += 1
                    
                    del future_to_num[future]
                    total_reports += 1
                    
                    # Progress update
                    if total_reports % 10 == 0:
                        show_progress(total_reports)
                    
                    # 121x cycle celebration
                    if total_reports % 121 == 0:
                        print(Fore.MAGENTA + Style.BRIGHT + f"\n🎉 121x CYCLE COMPLETE! 🎉")
                        print(Fore.CYAN + f"📊 Total reports: {total_reports} | Success rate: {(stats['successful']/stats['total_reports']*100):.1f}%")
                        print(Fore.YELLOW + "💀 Continuing the assault... 💀\n")
                    
                    # Random delay with jitter
                    delay = base_delay + random.uniform(-0.1, 0.3)
                    delay = max(0.2, min(delay, 1.0))
                    
                    if burst_mode and total_reports % 50 == 0:
                        # Brief pause in burst mode to avoid rate limits
                        time.sleep(random.uniform(1, 3))
                    else:
                        time.sleep(delay)
                    
                    break  # Exit as_completed to re-submit
                    
        except KeyboardInterrupt:
            print(Fore.YELLOW + f"\n\n⚠️ INTERRUPTED BY USER")
            print(Fore.CYAN + f"📊 Final Statistics:")
            print(Fore.GREEN + f"✅ Total reports sent: {total_reports}")
            print(Fore.CYAN + f"📈 Success rate: {(stats['successful']/max(1, stats['total_reports'])*100):.1f}%")
            return

def batch_report(targets_file):
    """Send reports to multiple targets from a file"""
    if not os.path.exists(targets_file):
        print(Fore.RED + f"❌ File {targets_file} not found!")
        return
    
    with open(targets_file, 'r') as f:
        targets = [line.strip() for line in f if line.strip()]
    
    print(Fore.CYAN + f"\n📋 Loaded {len(targets)} targets from {targets_file}")
    confirm = input(Fore.YELLOW + f"Send reports to all {len(targets)} targets? (y/n): ").lower()
    
    if confirm == 'y':
        threads = int(input("Threads (default 5): ") or "5")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for idx, target in enumerate(targets, 1):
                if check_blacklist(target):
                    print(Fore.YELLOW + f"⚠️ Skipping blacklisted target: {target}")
                    continue
                futures.append(executor.submit(vortex_report, target, idx))
            
            for future in as_completed(futures):
                if future.result():
                    print(Fore.GREEN + "✅ Batch report sent")
                else:
                    print(Fore.RED + "❌ Batch report failed")

# ---------- LOGIN SYSTEM ----------
def login():
    username = "vortex"
    password = "vortex killer"
    attempts = 0
    
    while attempts < 3:
        clear()
        banner()
        print(Fore.CYAN + "\n" + "="*50)
        print(Fore.YELLOW + "🔐 AUTHORIZATION REQUIRED")
        print(Fore.CYAN + "="*50)
        
        u = input(Fore.CYAN + "👤 Username: ").strip()
        p = getpass.getpass("🔒 Password: ").strip()
        
        if u == username and p == password:
            print(Fore.GREEN + "\n✅ ACCESS GRANTED - WELCOME COMMANDER")
            print(Fore.YELLOW + "⚡ Loading systems...")
            time.sleep(1.5)
            
            # Test network and email accounts
            if not network_test():
                print(Fore.RED + "⚠️ Network issues detected - continuing anyway...")
            
            test_email_accounts()
            
            stats["start_time"] = datetime.now().isoformat()
            save_stats()
            
            return True
        else:
            attempts += 1
            print(Fore.RED + f"\n❌ ACCESS DENIED - Invalid credentials ({3-attempts} attempts remaining)")
            time.sleep(2)
    
    print(Fore.RED + "\n💀 MAXIMUM ATTEMPTS EXCEEDED - SYSTEM LOCKED")
    return False

# ---------- MAIN MENU ----------
def main_menu():
    while True:
        clear()
        banner()
        show_stats()
        
        print(Fore.CYAN + "╔════════════════════════════════════════╗")
        print(Fore.YELLOW + "║            MAIN OPERATIONS             ║")
        print(Fore.CYAN + "╠════════════════════════════════════════╣")
        print(Fore.GREEN + "║ [1] 📩 Unban Temporary                 ║")
        print(Fore.GREEN + "║ [2] 🚫 Unban Permanent                 ║")
        print(Fore.GREEN + "║ [3] 🔍 Check Number                    ║")
        print(Fore.GREEN + "║ [4] ⚠️ Fraud Report                    ║")
        print(Fore.RED + Style.BRIGHT + "║ [5] 💀 ALPHA TERMINATE (INFINITE)      ║")
        print(Fore.CYAN + "╠════════════════════════════════════════╣")
        print(Fore.YELLOW + "║ [6] 📊 View Statistics                 ║")
        print(Fore.YELLOW + "║ [7] 📋 Batch Report (Multiple)         ║")
        print(Fore.YELLOW + "║ [8] 🚫 Blacklist Management            ║")
        print(Fore.YELLOW + "║ [9] 🔧 Test Email Accounts             ║")
        print(Fore.RED + "║ [0] ❌ Exit System                       ║")
        print(Fore.CYAN + "╚════════════════════════════════════════╝")
        
        choice = input(Fore.CYAN + "\n⚡ Select Operation: ").strip()
        
        if choice == "5":
            target = input("📞 Target Number (+2348012345678): ").strip()
            if re.match(r"^\+\d{10,15}$", target):
                if check_blacklist(target):
                    print(Fore.RED + "⚠️ Target is blacklisted!")
                    if input("Override? (y/n): ").lower() != 'y':
                        continue
                
                print(Fore.RED + Style.BRIGHT + "\n⚠️  ALPHA TERMINATE MODE - EXTREME CAUTION ⚠️")
                confirm = input(Fore.YELLOW + f"💀 Initiate INFINITE TURBO on {target}? (y/n): ").lower()
                
                if confirm == "y":
                    try:
                        threads = int(input("🔫 Threads (1-20, default 8): ") or "8")
                        threads = min(max(threads, 1), 20)
                        delay = float(input("⏱️ Delay (0.2-2.0, default 0.3): ") or "0.3")
                        delay = max(0.2, min(delay, 2.0))
                        burst = input("🚀 Burst Mode? (y/n, default n): ").lower() == 'y'
                        
                        turbo_terminate(target, threads=threads, base_delay=delay, burst_mode=burst)
                    except ValueError:
                        turbo_terminate(target)
                else:
                    print(Fore.YELLOW + "Operation cancelled")
            else:
                print(Fore.RED + "❌ Invalid number format! Use +[country code][number]")
                
        elif choice == "6":
            show_stats()
            input(Fore.CYAN + "\nPress Enter to continue...")
            
        elif choice == "7":
            file_path = input("📁 Path to targets file (one per line): ").strip()
            batch_report(file_path)
            input(Fore.CYAN + "\nPress Enter to continue...")
            
        elif choice == "8":
            print(Fore.YELLOW + "\n🚫 BLACKLIST MANAGEMENT")
            print("1. Add number to blacklist")
            print("2. View blacklist")
            print("3. Clear blacklist")
            bl_choice = input("Select: ")
            
            if bl_choice == "1":
                number = input("Number to blacklist: ").strip()
                add_to_blacklist(number)
            elif bl_choice == "2" and os.path.exists(BLACKLIST_FILE):
                with open(BLACKLIST_FILE, 'r') as f:
                    print(Fore.CYAN + f.read())
            elif bl_choice == "3":
                if input("Clear all blacklisted numbers? (y/n): ").lower() == 'y':
                    open(BLACKLIST_FILE, 'w').close()
                    print(Fore.GREEN + "Blacklist cleared!")
            input(Fore.CYAN + "\nPress Enter to continue...")
            
        elif choice == "9":
            test_email_accounts()
            input(Fore.CYAN + "\nPress Enter to continue...")
            
        elif choice == "0":
            print(Fore.RED + Style.BRIGHT + "\n💀 ALPHA BAN PREMIUM OFFLINE")
            print(Fore.YELLOW + f"📊 Final Statistics: {stats['total_reports']} total reports")
            print(Fore.CYAN + "👋 Stay brutal, stay anonymous\n")
            break
            
        else:
            print(Fore.YELLOW + "\n⚠️ Select 5 for TERMINATE or other valid options")
            time.sleep(2)

if __name__ == "__main__":
    load_stats()
    if login():
        main_menu()
