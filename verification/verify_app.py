
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get absolute path to index.html
        cwd = os.getcwd()
        url = f"file://{cwd}/index.html"

        print(f"Navigating to {url}")
        page.goto(url)

        # Wait for app to load
        page.wait_for_selector("h1", state="visible")

        # Screenshot Dashboard
        print("Taking screenshot of Dashboard")
        page.screenshot(path="verification/dashboard.png")

        # Go to Tasks
        print("Navigating to Tasks")
        page.get_by_role("link", name="Tasks").click()
        page.wait_for_timeout(500) # Wait for transition
        page.screenshot(path="verification/tasks.png")

        # Add a task
        print("Adding a task")
        page.get_by_placeholder("Add a new chore...").fill("Test Task to Delete")
        page.get_by_role("button").filter(has_text="plus").click() # Assuming plus icon is in button
        # Or just click the submit button
        # The button has a Plus icon.
        # Let's try clicking the button in the form.
        page.locator("form button").click()

        page.wait_for_timeout(500)
        page.screenshot(path="verification/tasks_added.png")

        # Find the delete button for the new task and click it.
        # The delete button was added with Trash icon.
        # It should be the last button in the task div.
        print("Deleting the task")
        # We can try to find the task by text, then find the button inside.
        task_locator = page.locator("div").filter(has_text="Test Task to Delete").last
        # The delete button is inside this div.
        # It has a Trash icon (svg).
        delete_btn = task_locator.locator("button").last
        delete_btn.click()

        page.wait_for_timeout(500)
        page.screenshot(path="verification/tasks_deleted.png")

        # Check Groceries
        print("Navigating to Shop")
        page.get_by_role("link", name="Shop").click()
        page.wait_for_timeout(500)
        page.screenshot(path="verification/groceries.png")

        # Add Grocery
        print("Adding grocery")
        page.get_by_placeholder("Add item").fill("Test Apple")
        page.locator("form button").click()
        page.wait_for_timeout(500)

        # Delete Grocery
        print("Deleting grocery")
        grocery_locator = page.locator("li").filter(has_text="Test Apple").last
        grocery_locator.locator("button").click()
        page.wait_for_timeout(500)
        page.screenshot(path="verification/groceries_deleted.png")

        browser.close()

if __name__ == "__main__":
    run()
