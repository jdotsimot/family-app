
from playwright.sync_api import sync_playwright

def verify_features():
    print("Verifying Features...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8000")

        page.wait_for_timeout(2000)

        # Go to Tasks page
        print("Navigating to Tasks...")
        page.get_by_role("link", name="Tasks").click()
        page.wait_for_selector("select") # Wait for select to appear

        # Verify Options
        print("Verifying Select Options...")
        options = page.locator("select option").all_inner_texts()
        expected_members = ["Mom", "Dad", "Jaidin", "Dausyn", "Grandma", "Grandpa"]

        missing = [m for m in expected_members if m not in options]
        if missing:
            print(f"Missing members in options: {missing}")
            print(f"Found options: {options}")
            return False
        else:
            print("All family members found in dropdown.")

        # Verify Mail Button existence
        # We look for the buttons. There should be at least one if there are tasks (test-task-1 should be there from previous run)
        # The mail button is distinguished by its click handler which we can't easily see, but we can count buttons.
        # Previously there was 1 button (trash) per row. Now there should be 2.

        # Let's take a screenshot to be sure.
        page.screenshot(path="verification/feature_verification.png")

        # Try to find the button visually or by order?
        # We added it *before* the trash button.

        # Let's just check if we can see more buttons than tasks * 1.
        # Assuming we have 1 task.
        buttons = page.locator("div.space-y-3 > div button").count()
        print(f"Found {buttons} buttons in task list.")
        if buttons >= 2:
             print("Mail button likely present (count >= 2 per task).")
        else:
             print("Mail button missing?")
             return False

        browser.close()
    return True

if __name__ == "__main__":
    if verify_features():
        print("Feature Verification Passed.")
    else:
        print("Feature Verification Failed.")
        exit(1)
