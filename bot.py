import time
import random
import os
import sys
import json
import pyotp
import threading
from concurrent.futures import ThreadPoolExecutor
from seleniumbase import SB
from colorama import Fore, Style, init
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich import box

# ═══════════════════════════════════════════════════════════════════
# 🎨 CẤU HÌNH TOOL
# ═══════════════════════════════════════════════════════════════════
TOOL_NAME = "X-ENGAGE BOT"
VERSION = "v6.0 PRO"
PROFILE_DIR = os.path.join(os.getcwd(), "ENGAGE BOT_profiles")
CONFIG_FILE = os.path.join(os.getcwd(), "profile_config.json")

if not os.path.exists(PROFILE_DIR):
    os.makedirs(PROFILE_DIR)

WIN_WIDTH = 380
WIN_HEIGHT = 700
COLS_PER_ROW = 5

REPORT_DATA = []
REPORT_LOCK = threading.Lock()
init(autoreset=True)
console = Console()

# ═══════════════════════════════════════════════════════════════════
# 🎭 ANTI-DETECT: Tạo danh tính độc lập
# ═══════════════════════════════════════════════════════════════════
def load_profile_configs():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_profile_configs(configs):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(configs, f, indent=2, ensure_ascii=False)

def generate_profile_identity(username):
    configs = load_profile_configs()
    
    if username in configs:
        return configs[username]
    
    # Fake UserAgent list
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    identity = {
        'user_agent': random.choice(user_agents),
        'screen_resolution': random.choice(['1920x1080', '1366x768', '1536x864', '1440x900']),
        'platform': random.choice(['Win32', 'MacIntel', 'Linux x86_64']),
        'language': random.choice(['en-US', 'en-GB', 'vi-VN']),
        'device_memory': random.choice([4, 8, 16, 32]),
        'hardware_concurrency': random.choice([2, 4, 8, 12, 16])
    }
    
    configs[username] = identity
    save_profile_configs(configs)
    return identity

# ═══════════════════════════════════════════════════════════════════
# 🎨 GIAO DIỆN SẠCH ĐẸP (ĐÃ UPDATE CONTACT)
# ═══════════════════════════════════════════════════════════════════
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    
    # Tạo ASCII Art chữ X-ENGAGE BOT
    try:
        ascii_art = pyfiglet.figlet_format("X - ENGAGE BOT", font="slant")
    except:
        ascii_art = "X - ENGAGE BOT" 

    # Tạo nội dung Banner
    text_content = Text()
    text_content.append(ascii_art, style="bold cyan")
    text_content.append("\n")
    
    # --- PHẦN CONTACT TÁC GIẢ (Đã chỉnh sửa để không bị mất) ---
    author_text = Text(" Nguyễn Trọng Huấn ", style="bold black on yellow")
    donate = Text(" MB Bank: 9886786789 ", style="bold black on yellow")
    text_content.append(author_text)
    text_content.append("\n\n")
    text_content.append(donate)
    text_content.append("\n\n")
    # -----------------------------------------------------------

    text_content.append("──────────────────────────────────────────────────────────\n", style="dim white")
    text_content.append("⚡ Anti-Detect  •  👤 Human Behavior  •  🔔 Smart Follow", style="bold white")

    # Hiển thị Panel
    panel = Panel(
        Align.center(text_content),
        title=f"[bold green]🔥 {VERSION} 🔥[/bold green]",
        # THÊM CONTACT VÀO CẠNH DƯỚI CỦA KHUNG LUÔN CHO CHẮC
        subtitle="[bold yellow]🚀 Author: t.me/tomnuongcay 🚀[/bold yellow]", 
        border_style="bright_blue",
        box=box.DOUBLE, 
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()

def show_menu():
    console.print("╔════════════════════ MENU CHỨC NĂNG ════════════════════╗", style="bold green")
    console.print("║                                                         ║", style="green")
    console.print("║  [1]  🎯  Auto Like Feed                                ║", style="bold white")
    console.print("║  [2]  👥  Target Follow (Smart Subscribe Check)         ║", style="bold white")
    console.print("║  [3]  🌱  Nuôi Nick (Human Behavior)                    ║", style="bold white")
    console.print("║  [4]  🔧  Mở Profile Thủ Công                           ║", style="bold white")
    console.print("║  [5]  📊  Xem Danh Sách Profile                         ║", style="bold white")
    console.print("║  [0]  🚪  Thoát                                         ║", style="bold white")
    console.print("║                                                         ║", style="green")
    console.print("╚═════════════════════════════════════════════════════════╝", style="bold green")
    console.print()

# ═══════════════════════════════════════════════════════════════════
# 🤖 HUMAN BEHAVIOR
# ═══════════════════════════════════════════════════════════════════
def human_delay(min_sec=5, max_sec=7):
    time.sleep(random.uniform(min_sec, max_sec))

def smooth_scroll(sb, direction='down', intensity='medium'):
    if intensity == 'light':
        pixels = random.randint(200, 400)
        steps = random.randint(3, 5)
    elif intensity == 'medium':
        pixels = random.randint(400, 700)
        steps = random.randint(5, 8)
    else:
        pixels = random.randint(700, 1200)
        steps = random.randint(8, 12)
    
    step_size = pixels // steps
    for _ in range(steps):
        sb.execute_script(f"window.scrollBy(0, {step_size if direction == 'down' else -step_size});")
        time.sleep(random.uniform(0.1, 0.3))

def random_mouse_movement(sb):
    try:
        x = random.randint(100, 500)
        y = random.randint(100, 500)
        sb.execute_script(f"""
            var event = new MouseEvent('mousemove', {{
                'clientX': {x},
                'clientY': {y}
            }});
            document.dispatchEvent(event);
        """)
    except:
        pass

def human_type(sb, selector, text, username):
    try:
        sb.wait_for_element_visible(selector, timeout=15)
        console.print(f"[dim]💬 [{username}] Đang nhập...[/dim]")
        sb.click(selector)
        time.sleep(random.uniform(1, 2))
        
        for char in text:
            sb.send_keys(selector, char)
            if random.random() < 0.1:
                time.sleep(random.uniform(0.5, 1.5))
            else:
                time.sleep(random.uniform(0.08, 0.25))
        
        human_delay(2, 3)
        return True
    except:
        return False

def get_2fa_code(secret_key):
    try:
        return pyotp.TOTP(secret_key.replace(" ", "")).now()
    except:
        return None

# ═══════════════════════════════════════════════════════════════════
# 🎯 LOGIC THỰC THI
# ═══════════════════════════════════════════════════════════════════
def simulate_reading(sb, username):
    console.print(f"[dim]📖 [{username}] Đang đọc...[/dim]")
    time.sleep(random.uniform(2, 5))
    random_mouse_movement(sb)

def run_action_logic(sb, choice, config, username):
    try:
        if choice == "1":  # Auto Like
            console.print(f"[yellow]🎯 [{username}] Bắt đầu Like...[/yellow]")
            sb.open("https://x.com/home")
            human_delay(3, 5)
            
            num_likes = random.randint(3, 6)
            liked_count = 0
            
            for i in range(num_likes):
                smooth_scroll(sb, 'down', random.choice(['light', 'medium']))
                human_delay(2, 4)
                simulate_reading(sb, username)
                
                try:
                    if sb.is_element_visible('[data-testid="like"]'):
                        sb.click('[data-testid="like"]')
                        liked_count += 1
                        console.print(f"[green]❤️  [{username}] Like #{liked_count}[/green]")
                except:
                    pass
                
                human_delay(3, 6)
            
            console.print(f"[bold green]✅ [{username}] Xong: {liked_count} likes[/bold green]")
        
        elif choice == "2":  # Target Follow
            targets = config.get('targets', [])
            console.print(f"[yellow]👥 [{username}] Follow {len(targets)} target...[/yellow]")
            
            for idx, t in enumerate(targets, 1):
                t = t.strip()
                if not t:
                    continue
                
                console.print(f"[cyan]🎯 [{username}] [{idx}/{len(targets)}] @{t}[/cyan]")
                sb.open(f"https://x.com/{t}")
                human_delay(3, 5)
                
                smooth_scroll(sb, 'down', 'light')
                simulate_reading(sb, username)
                smooth_scroll(sb, 'up', 'light')
                
                # Selectors
                follow_btn = '[aria-label*="Follow"][role="button"]:not([aria-label*="Following"])'
                following_btn = '[aria-label*="Following"][role="button"]'
                subscribe_btn = '[aria-label*="Subscribe"][role="button"]'
                
                # Kiểm tra đã follow
                try:
                    if sb.is_element_visible(following_btn) or sb.is_element_visible(subscribe_btn):
                        console.print(f"[white]✓ [{username}] @{t} đã Follow[/white]")
                        continue
                except:
                    pass
                
                # Follow
                try:
                    sb.wait_for_element_visible(follow_btn, timeout=10)
                    console.print(f"[dim]👆 [{username}] Click Follow...[/dim]")
                    sb.click(follow_btn)
                    time.sleep(5)
                    
                    # Kiểm tra kết quả
                    is_following = sb.is_element_visible(following_btn)
                    is_subscribe = sb.is_element_visible(subscribe_btn)
                    text_following = sb.is_text_visible("Following")
                    text_subscribe = sb.is_text_visible("Subscribe")
                    
                    if is_following or is_subscribe or text_following or text_subscribe:
                        badge = "🔔" if (is_subscribe or text_subscribe) else "✅"
                        note = " (Subscribe)" if (is_subscribe or text_subscribe) else ""
                        console.print(f"[bold green]{badge} [{username}] SUCCESS @{t}{note}[/bold green]")
                    else:
                        console.print(f"[bold red]❌ [{username}] FAILED @{t}[/bold red]")
                except Exception as e:
                    console.print(f"[red]⚠️  [{username}] Lỗi @{t}: {str(e)[:30]}[/red]")
                
                human_delay(4, 7)
        
        elif choice == "3":  # Nuôi Nick
            t_min = config.get('t_min', 30)
            t_max = config.get('t_max', 60)
            duration = random.randint(t_min, t_max)
            
            console.print(f"[yellow]🌱 [{username}] Nuôi {duration}s...[/yellow]")
            sb.open("https://x.com/home")
            human_delay(2, 3)
            
            start_time = time.time()
            action_count = 0
            
            while time.time() - start_time < duration:
                intensity = random.choice(['light', 'medium', 'heavy'])
                smooth_scroll(sb, 'down', intensity)
                
                action = random.choice(['read', 'like', 'scroll', 'wait'])
                
                if action == 'read':
                    simulate_reading(sb, username)
                    action_count += 1
                elif action == 'like' and random.random() < 0.2:
                    try:
                        if sb.is_element_visible('[data-testid="like"]'):
                            sb.click('[data-testid="like"]')
                            console.print(f"[green]❤️  [{username}] Like random[/green]")
                            action_count += 1
                    except:
                        pass
                elif action == 'wait':
                    time.sleep(random.uniform(3, 8))
                
                random_mouse_movement(sb)
                human_delay(3, 6)
                
                elapsed = int(time.time() - start_time)
                if elapsed % 10 == 0:
                    console.print(f"[dim]⏱️  [{username}] {elapsed}/{duration}s | {action_count} acts[/dim]")
            
            console.print(f"[bold green]✅ [{username}] Xong | {action_count} actions[/bold green]")

    except Exception as e:
        console.print(f"[red]❌ [{username}] Lỗi: {str(e)[:50]}[/red]")

# ═══════════════════════════════════════════════════════════════════
# 🔧 MỞ PROFILE THỦ CÔNG
# ═══════════════════════════════════════════════════════════════════
def open_manual_profiles(accounts):
    console.print("\n[bold yellow]🔧 Chế độ mở Profile thủ công[/bold yellow]\n")
    
    # Danh sách
    for idx, acc in enumerate(accounts, 1):
        username = acc[0].strip()
        proxy = acc[3] if len(acc) > 3 else "No Proxy"
        console.print(f"  [{idx}] {username} | {proxy}")
    
    console.print()
    choice = input("Chọn profile (VD: 1,3,5 hoặc 'all'): ").strip()
    
    if choice.lower() == "all":
        selected = list(range(len(accounts)))
    else:
        try:
            selected = [int(x.strip())-1 for x in choice.split(",")]
        except:
            console.print("[red]❌ Lựa chọn không hợp lệ![/red]")
            return
    
    console.print(f"\n[green]✅ Đang mở {len(selected)} profile...[/green]\n")
    
    for idx in selected:
        if idx < 0 or idx >= len(accounts):
            continue
        
        acc_info = accounts[idx]
        username = acc_info[0].strip()
        proxy = acc_info[3] if len(acc_info) > 3 else None
        user_profile_path = os.path.join(PROFILE_DIR, username)
        
        pos_x = (idx % COLS_PER_ROW) * WIN_WIDTH
        pos_y = (idx // COLS_PER_ROW) * WIN_HEIGHT
        
        console.print(f"[cyan]🚀 Mở: {username}[/cyan]")
        
        threading.Thread(
            target=open_single_profile,
            args=(username, proxy, user_profile_path, pos_x, pos_y),
            daemon=True
        ).start()
        
        time.sleep(2)
    
    console.print("\n[green]✅ Đã mở xong! Nhấn Enter để quay menu...[/green]")
    input()

def open_single_profile(username, proxy, profile_path, pos_x, pos_y):
    identity = generate_profile_identity(username)
    
    with SB(uc=True, 
            proxy=proxy,
            user_data_dir=profile_path,
            window_size=f"{WIN_WIDTH},{WIN_HEIGHT}",
            chromium_arg=f"--window-position={pos_x},{pos_y},--force-device-scale-factor=0.8,--user-agent={identity['user_agent']}") as sb:
        
        sb.open("https://x.com/home")
        console.print(f"[green]✅ {username} sẵn sàng![/green]")
        
        while True:
            time.sleep(60)

# ═══════════════════════════════════════════════════════════════════
# 👷 WORKER
# ═══════════════════════════════════════════════════════════════════
def worker(acc_info, choice, config, index):
    username = acc_info[0].strip()
    password = acc_info[1].strip()
    twofa = acc_info[2].strip()
    proxy = acc_info[3] if len(acc_info) > 3 else None
    
    user_profile_path = os.path.join(PROFILE_DIR, username)
    identity = generate_profile_identity(username)
    
    pos_x = (index % COLS_PER_ROW) * WIN_WIDTH
    pos_y = (index // COLS_PER_ROW) * WIN_HEIGHT
    
    console.print(f"[cyan]🚀 [{username}] Khởi động Anti-Detect...[/cyan]")
    
    with SB(uc=True,
            proxy=proxy,
            user_data_dir=user_profile_path,
            window_size=f"{WIN_WIDTH},{WIN_HEIGHT}",
            chromium_arg=f"--window-position={pos_x},{pos_y},--force-device-scale-factor=0.8,--user-agent={identity['user_agent']}") as sb:
        
        try:
            # Anti-Detect Fingerprint
            sb.execute_script(f"""
                Object.defineProperty(navigator, 'hardwareConcurrency', {{
                    get: () => {identity['hardware_concurrency']}
                }});
                Object.defineProperty(navigator, 'deviceMemory', {{
                    get: () => {identity['device_memory']}
                }});
                Object.defineProperty(navigator, 'platform', {{
                    get: () => '{identity['platform']}'
                }});
            """)
            
            sb.open("https://x.com/home")
            human_delay(3, 5)
            
            # Kiểm tra login
            try:
                is_logged_in = sb.is_element_visible('[aria-label="Home"]')
            except:
                is_logged_in = False
            
            if not is_logged_in:
                console.print(f"[yellow]🔐 [{username}] Đang login...[/yellow]")
                
                sb.open("https://x.com/i/flow/login")
                human_delay(3, 4)
                
                # Username
                if human_type(sb, 'input[autocomplete="username"]', username, username):
                    sb.send_keys('input[autocomplete="username"]', "\n")
                    human_delay(3, 4)
                    
                    # Password
                    try:
                        sb.wait_for_element_visible('input[name="password"]', timeout=10)
                        human_type(sb, 'input[name="password"]', password, username)
                        sb.send_keys('input[name="password"]', "\n")
                        human_delay(3, 5)
                        
                        # 2FA
                        try:
                            sb.wait_for_element_visible('input[data-testid="ocfEnterTextTextInput"]', timeout=10)
                            code = get_2fa_code(twofa)
                            if code:
                                console.print(f"[cyan]🔢 [{username}] 2FA: {code}[/cyan]")
                                human_type(sb, 'input[data-testid="ocfEnterTextTextInput"]', code, username)
                                sb.send_keys('input[data-testid="ocfEnterTextTextInput"]', "\n")
                                human_delay(4, 6)
                        except:
                            pass
                    except:
                        pass
            
            # Kiểm tra login success
            time.sleep(3)
            current_url = sb.get_current_url()
            try:
                home_visible = sb.is_element_visible('[aria-label="Home"]')
            except:
                home_visible = False
            
            if "/home" in current_url or home_visible:
                console.print(f"[bold green]✅ [{username}] LOGIN SUCCESS[/bold green]")
                run_action_logic(sb, choice, config, username)
                result = "✅ SUCCESS"
            else:
                console.print(f"[red]❌ [{username}] LOGIN FAILED[/red]")
                result = "❌ FAILED"
            
            with REPORT_LOCK:
                REPORT_DATA.append((username, result))
        
        except Exception as e:
            console.print(f"[red]💥 [{username}] Lỗi: {str(e)[:50]}[/red]")
            with REPORT_LOCK:
                REPORT_DATA.append((username, f"❌ ERROR: {str(e)[:30]}"))

# ═══════════════════════════════════════════════════════════════════
# 📊 BÁO CÁO
# ═══════════════════════════════════════════════════════════════════
def show_report():
    if not REPORT_DATA:
        console.print("[yellow]⚠️  Chưa có dữ liệu[/yellow]")
        return
    
    console.print("\n╔════════════════════ BÁO CÁO KẾT QUẢ ═══════════════════╗", style="bold green")
    
    for idx, (username, result) in enumerate(REPORT_DATA, 1):
        style = "green" if "SUCCESS" in result else "red"
        console.print(f"║ [{idx}] {username:20s} | [{style}]{result}[/{style}]", style="white")
    
    console.print("╚═════════════════════════════════════════════════════════╝", style="bold green")
    
    # Stats
    success = sum(1 for _, r in REPORT_DATA if "SUCCESS" in r)
    failed = len(REPORT_DATA) - success
    
    console.print(f"\n[bold yellow]📈 THỐNG KÊ:[/bold yellow] ", end="")
    console.print(f"[bold green]✅ {success}[/bold green] | ", end="")
    console.print(f"[bold red]❌ {failed}[/bold red] | ", end="")
    console.print(f"[bold cyan]📊 Tổng: {len(REPORT_DATA)}[/bold cyan]\n")

def show_profile_list():
    configs = load_profile_configs()
    
    if not configs:
        console.print("\n[yellow]⚠️  Chưa có profile![/yellow]\n")
        input("Nhấn Enter...")
        return
    
    console.print("\n╔═══════════════ DANH SÁCH PROFILES ══════════════╗", style="bold cyan")
    
    for idx, (username, identity) in enumerate(configs.items(), 1):
        console.print(f"║ [{idx}] {username:20s} | {identity['platform']:15s} | {identity['device_memory']}GB RAM", style="white")
    
    console.print("╚═════════════════════════════════════════════════╝", style="bold cyan")
    console.print()
    input("Nhấn Enter...")

# ═══════════════════════════════════════════════════════════════════
# 🎮 MAIN
# ═══════════════════════════════════════════════════════════════════
def main():
    print_banner()
    
    if not os.path.exists("accounts.txt"):
        console.print("[red]❌ Không tìm thấy accounts.txt![/red]")
        console.print("[yellow]Format: username|password|2fa_secret|proxy[/yellow]")
        return
    
    with open("accounts.txt", "r", encoding="utf-8") as f:
        accounts = [line.strip().split("|") for line in f if "|" in line]
    
    if not accounts:
        console.print("[red]❌ File accounts.txt trống![/red]")
        return
    
    console.print(f"[green]✅ Đã load {len(accounts)} tài khoản[/green]\n")
    
    while True:
        show_menu()
        choice = input("Chọn [0-5]: ").strip()
        
        if choice == "0":
            console.print("\n[yellow]👋 Tạm biệt![/yellow]\n")
            break
        
        elif choice == "4":
            open_manual_profiles(accounts)
            print_banner()
            continue
        
        elif choice == "5":
            show_profile_list()
            print_banner()
            continue
        
        elif choice in ["1", "2", "3"]:
            config = {}
            
            if choice == "2":
                targets_input = input("\n👥 Nhập list user (elonmusk,nasa): ").strip()
                config['targets'] = targets_input.split(",")
            
            elif choice == "3":
                config['t_min'] = int(input("\n⏱️  Min giây: ").strip() or "30")
                config['t_max'] = int(input("⏱️  Max giây: ").strip() or "60")
            
            num_threads = int(input("\n🔢 Số thread: ").strip() or "5")
            
            REPORT_DATA.clear()
            
            console.print(f"\n[bold green]🚀 BẮT ĐẦU CHẠY {num_threads} THREADS...[/bold green]\n")
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                for i, acc in enumerate(accounts):
                    executor.submit(worker, acc, choice, config, i)
                    time.sleep(3)
            
            show_report()
            input("\nNhấn Enter để quay menu...")
            print_banner()
        
        else:
            console.print("[red]❌ Lựa chọn không hợp lệ![/red]")
            time.sleep(1)

if __name__ == "__main__":
    main()
