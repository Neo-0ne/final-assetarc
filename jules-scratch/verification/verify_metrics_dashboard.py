import os
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to the local HTML file
        # The script is in jules-scratch/verification, the file is in assetarc-theme/templates
        # So we need to go up two directories from the script's location.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, '..', '..', 'assetarc-theme', 'templates', 'template-metrics.php')

        # Check if file exists before trying to navigate
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Could not find the template file at: {file_path}")

        # Navigate to the local file
        page.goto(f'file://{file_path}')

        # Wait for the "Total Revenue" element to not say "Loading..."
        # This confirms the fetch call has completed.
        revenue_locator = page.locator("#total-revenue")
        expect(revenue_locator).not_to_have_text("Loading...", timeout=10000) # 10s timeout

        # Wait for the "Total Transactions" element to not say "Loading..."
        transactions_locator = page.locator("#total-transactions")
        expect(transactions_locator).not_to_have_text("Loading...")

        # Take a screenshot for visual verification
        screenshot_path = os.path.join(script_dir, 'verification.png')
        page.screenshot(path=screenshot_path)

        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    run_verification()
