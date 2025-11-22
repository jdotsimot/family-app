
import requests
import time
import json
import os
from playwright.sync_api import sync_playwright

def verify_persistence_workflow():
    print("Verifying Full Persistence Workflow...")
    base_url = "http://localhost:8000"

    # 1. Ensure starting clean (no data.json on server)
    # We can't easily delete file on server via API, but we can rely on previous step.
    # We will assume server is fresh or we just deleted data.json.

    # 2. Verify App Loads with Default Data
    print("Step 1: Loading App to initialize state...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url)

        # Wait for load
        try:
            page.wait_for_selector("text=Family App", timeout=5000)
            print("App loaded successfully.")
        except:
            print("App failed to load!")
            page.screenshot(path="verification/failure_load.png")
            return False

        # Allow time for initial fetch (404) and save (POST)
        page.wait_for_timeout(2000)

        page.screenshot(path="verification/step1_initial_load.png")
        browser.close()

    # 3. Verify data.json was created and has default data
    print("Step 2: Checking if data was saved to server...")
    try:
        resp = requests.get(f"{base_url}/api/data")
        if resp.status_code != 200:
            print(f"Failed to get data: {resp.status_code}")
            return False

        data = resp.json()
        # Check for some expected default keys
        if "events" in data and "tasks" in data:
            print("Server has valid data structure.")
        else:
            print(f"Server data invalid: {data.keys()}")
            return False
    except Exception as e:
        print(f"Error checking server data: {e}")
        return False

    # 4. Modify data via API (simulate another user)
    print("Step 3: Modifying data via API...")
    new_task = {"id": "test-task-1", "title": "Verify Persistence", "assignee": "Jules", "status": "todo"}
    data["tasks"].append(new_task)

    try:
        resp = requests.post(f"{base_url}/api/data", json=data)
        if resp.status_code != 200:
            print("Failed to post updated data")
            return False
    except Exception as e:
        print(f"Error posting data: {e}")
        return False

    # 5. Reload App and Verify New Data appears
    print("Step 4: Reloading App to verify new data...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url)

        # Navigate to tasks page
        # The nav structure isn't fully known but we can try to find the task text
        # Or just wait and see if it appears in a dashboard list if applicable.
        # The dashboard shows "Pending Chores", maybe it lists them?
        # Let's look for the text "Verify Persistence"

        try:
            # Wait for fetch
            page.wait_for_timeout(2000)

            # Go to Tasks page (click "Tasks" link)
            page.get_by_role("link", name="Tasks").click()

            page.wait_for_selector("text=Verify Persistence", timeout=5000)
            print("Found new task in UI!")
            page.screenshot(path="verification/step4_persistence_verified.png")
        except Exception as e:
            print(f"Failed to find new task in UI: {e}")
            page.screenshot(path="verification/failure_verification.png")
            return False

        browser.close()

    print("Full Persistence Verification Passed.")
    return True

if __name__ == "__main__":
    if verify_persistence_workflow():
        exit(0)
    else:
        exit(1)
