import csv
from playwright.sync_api import sync_playwright

# Create or open the CSV file for logging
def create_csv_file():
    with open('network_requests.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header row (you can modify this based on what you want to log)
        writer.writerow(['Type', 'Method/Status', 'URL', 'Request Body'])

# Log data to CSV file
def log_to_csv(request_type, method_or_status, url, request_body=None):
    with open('network_requests.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write a row for each request or response
        writer.writerow([request_type, method_or_status, url, request_body])

def run():
    with sync_playwright() as p:
        # Launch the browser (headless=False so we can see the browser window)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Listen for 'request' event to capture network requests
        def handle_request(request):
            # Access the post_data attribute directly (no parentheses)
            log_to_csv('Request', request.method, request.url, request.post_data)  # Log request details

        # Listen for 'response' event to capture network responses
        def handle_response(response):
            log_to_csv('Response', response.status, response.url)  # Log response details

        # Subscribe to 'request' and 'response' events
        page.on('request', handle_request)
        page.on('response', handle_response)

        # Go to the website of interest
        page.goto('https://www.timelessha.com/')  # Replace with your target URL

        # Wait for the page to finish loading (all requests to complete)
        page.wait_for_load_state('networkidle', timeout=10000)  # Wait until there is no network activity for 10000ms

        # Close the page and browser after capturing requests
        page.close()
        browser.close()

if __name__ == "__main__":
    create_csv_file()  # Create the CSV file and add the header
    run()
