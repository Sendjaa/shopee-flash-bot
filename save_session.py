import asyncio
from playwright.async_api import async_playwright
async def save_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto('https://shopee.co.id/buyer/login')

        print("Please log in to your Shopee account. After logging in, the session will be saved.")
        print("Tutup terminal ini setelah Anda selesai login.")
        
        try:
            await asyncio.sleep(60)
        except asyncio.CancelledError:
            pass

        await context.storage_state(path='session.json')
        print("Session saved to session.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(save_session())