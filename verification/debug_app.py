
from playwright.sync_api import sync_playwright

def debug_app():
    print("Debugging App...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Capture console logs
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        # Capture page errors
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))

        try:
            response = page.goto("http://localhost:8000")
            print(f"Navigation response status: {response.status}")
        except Exception as e:
            print(f"Navigation failed: {e}")

        page.wait_for_timeout(3000)

        print(f"Page Title: {page.title()}")
        print(f"Content: {page.content()[:500]}...")

        browser.close()

if __name__ == "__main__":
    debug_app()
