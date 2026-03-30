import asyncio
from playwright.async_api import async_playwright
import time
import sys
from utils import print_banner, show_menu, clear_screen, load_config

async def run_war():
    conf = load_config()
    
    async with async_playwright() as p:
        print("\n[!] Menghubungkan ke Chrome...")
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0]
        except Exception as e:
            print(f"[-] ERROR: {e}. Pastikan Chrome Port 9222 Aktif!")
            return

        print(f"[+] STANDBY DI: {page.url}")
        
        while True:
            t_skrg = time.strftime("%Y-%m-%d %H:%M:%S")
            if t_skrg >= conf['WAKTU_WAR']:
                break
            await asyncio.sleep(0.001)

        print("\n[!!!] WAR START! [!!!]")
        await page.reload(wait_until="commit")
        await asyncio.sleep(conf['RELOAD_DELAY'])
        
        start_war = time.time()
        while time.time() - start_war < 45:
            try:
                if "checkout" not in page.url:
                    # Klik Beli Sekarang
                    btn_beli = page.locator('button.YuENex, button:has-text("Beli Sekarang")').last
                    if await btn_beli.count() > 0:
                        await btn_beli.click(force=True, no_wait_after=True)
                        print("[*] Mencoba klik Beli...")
                else:
                    btn_check = page.locator('button:has-text("Buat Pesanan"), button.stardust-button--primary').last
                    if await btn_check.count() > 0:
                        await btn_check.click(force=True, delay=conf['CLICK_DELAY'])
                        print("[***] BERHASIL BUAT PESANAN! [***]")
                        return 
            except:
                pass
            await asyncio.sleep(0.2)

async def main():
    while True:
        clear_screen()
        print_banner()
        pilihan = show_menu()

        if pilihan == '1':
            await run_war()
            input("\nSelesai. Tekan Enter untuk ke menu...")
        elif pilihan == '2':
            print("\n[!] Mengecek Port 9222...")
            time.sleep(1)
            print("[+] Port Terdeteksi! Chrome Siap.")
            time.sleep(2)
        elif pilihan == '3':
            print("\nSampai jumpa, Sendjaa!")
            sys.exit()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit()