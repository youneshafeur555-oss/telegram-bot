تـم فـك الاداه 👋🏿💔
#طـيِـف فـي كـل مكان😂❤
#nnlnn1
import requests
import time
import os
import random
import webbrowser
from colorama import Fore, Back, Style, init

# تهيئة الألوان
init(autoreset=True)

def optional_subscribe():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + Style.BRIGHT + "╔═════════════════════════════════════════════════╗")
    print(Fore.GREEN + Style.BRIGHT + "║    تـم تشـغيل مـن قبل طـيِـف    ║")
    print(Fore.GREEN + Style.BRIGHT + "╚══════════════════════════════════════════════════╝\n")

    print(Fore.CYAN + " [+] أهلاً بك ����")
    print(Fore.YELLOW + " [!] جاري تحويلك لقناة المطور للحصول على التحديثات...")
    time.sleep(1.5)

    # محاولة فتح القناة (دعاية فقط)
    try:
        webbrowser.open("https://t.me/zzxa17")
    except:
        pass

    print(Fore.GREEN + "\n [✔] يمكنك الآن البدء باستخدام الأداة مباشرة.")
    print(Fore.WHITE + " " + "="*50)
    # هنا جعلنا الضغط على Enter مجرد شكل للانتقال وليس إجبارياً للتحقق
    input(Fore.YELLOW + " [>] اضغط (Enter) لفتح واجهة التحكم... ")

def canaan_matrix_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + Style.BRIGHT + """
    ╦══════════════════════════════════════════════════════════╦
    ║                                                          ║
    ║   ██████╗ █████╗ ███╗   ██╗ █████╗  █████╗ ███╗   ██╗    ║
    ║  ██╔════╝██╔══██╗████╗  ██║██╔══██╗██╔══██╗████╗  ██║    ║
    ║  ██║     ███████║██╔██╗ ██║███████║███████║██╔██╗ ██║    ║
    ║  ██║     ██╔══██║██║╚██╗██║██╔══██║██╔══██║██║╚██╗██║    ║
    ║  ╚██████╗██║  ██║██║ ╚████║██║  ██║██║  ██║██║ ╚████║    ║
    ║   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ║
    ║                                                          ║
    ╠══════════════════════════════════════════════════════════╣
     طـيِـف هـنا🇦🇱                                                    
    ╩══════════════════════════════════════════════════════════╩
    """)

def canaan_reporting_logic(target_id, session_id, report_type):
    url = "https://www.tiktok.com/api/report/action/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-N960F)",
        "Cookie": f"sessionid={session_id}",
    }
    payload = {
        "target_id": target_id,
        "report_type": report_type,
        "reason": "Violation of Privacy",
        "source": "profile_more"
    }
    try:
        res = requests.post(url, headers=headers, data=payload, timeout=10)
        return res.status_code == 200
    except:
        return False

def main():
    # تشغيل رسالة الترحيب الاختيارية
    optional_subscribe()

    # واجهة الأداة
    canaan_matrix_banner()

    print(Fore.WHITE + Style.BRIGHT + " ⟪ إعــــدادات الــهــجــوم ⟫")
    target = input(Fore.CYAN + " ➦ يوزر الهدف: " + Fore.WHITE)
    session = input(Fore.CYAN + " ➦ كود الجلسة (Session ID): " + Fore.WHITE)

    print("\n" + Fore.RED + Style.BRIGHT + " ⟪ أنواع بلاغات الحجي بل قياده👻 ⟫")
    print(Fore.WHITE + "  [1] انتحال شخصية")
    print(Fore.WHITE + "  [2] انتهاك خصوصية")
    print(Fore.WHITE + "  [3] محتوى مخالف")

    choice = input(Fore.CYAN + "\n ➦ اختر (1-3): " + Fore.WHITE)
    try:
        count = int(input(Fore.CYAN + " ➦ عدد البلاغات: " + Fore.WHITE))
    except:
        count = 1

    print(Fore.GREEN + Style.BRIGHT + f"\n [⚡] جاري البدء ☠️🚬 ...\n")

    for i in range(count):
        print(Fore.YELLOW + f" [⟳] جاري ضخ البلاغ رقم ({i+1})...", end="\r")
        status = canaan_reporting_logic(target, session, choice)
        if status:
            print(Fore.GREEN + f" [✔] تم إرسال البلاغ ({i+1}) بنجاح.  ")
        else:
            print(Fore.RED + f" [✘] فشل البلاغ ({i+1}). راجع الجلسة.  ")
        time.sleep(1.5)

    print("\n" + Fore.GREEN + Style.BRIGHT + " ╔════════════════════════════════════════╗")
    print(Fore.CYAN  + Style.BRIGHT + " ║ [★] تـمت العمليه: طـيف هنا👻  ║")
    print(Fore.GREEN + Style.BRIGHT + " ╚════════════════════════════════════════╝")
    input(Fore.WHITE + "\n اضغط (Enter) للخروج...")

