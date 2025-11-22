from playwright.sync_api import sync_playwright

def verify_app_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8000")

        # Wait for something to load. The app title in HTML is "Family App"
        # We can also wait for the root div to not be empty, or check for specific content if we knew what it was.
        # Since I don't know the content, I'll take a screenshot and check the title.

        print(f"Page title: {page.title()}")

        # Give it a second to execute JS
        page.wait_for_timeout(2000)

        page.screenshot(path="verification/app_screenshot.png")
        browser.close()

if __name__ == "__main__":
    verify_app_loads()
