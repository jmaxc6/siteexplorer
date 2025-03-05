import re
import csv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from playwright.sync_api import sync_playwright
import time
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # Ensures consistent language detection

app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app)

def check_page_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Handle unexpected dialogs (alerts, confirms, prompts)
        page.on("dialog", lambda dialog: dialog.dismiss())
        
        try:
            print(f"Processing: {url}")
            page.goto(url, timeout=60000)
            page.wait_for_load_state('networkidle')

            # Attempt to dismiss pop-ups by pressing Escape
            for _ in range(3):  # Try up to 3 times
                time.sleep(1)  # Allow time for pop-ups to appear
                page.keyboard.press("Escape")
            
            page_text = page.inner_text("body").lower()
            has_privacy = "privacy" in page_text
            has_tos = "terms" in page_text 
            
            try:
                detected_language = detect(page_text)
            except Exception:
                detected_language = "unknown"
            
            print(f"Results for {url} -> Privacy Policy: {'Y' if has_privacy else 'N'}, Terms of Service: {'Y' if has_tos else 'N'}, Language: {detected_language}")
        
        except Exception as e:
            print(f"Error loading {url}: {e}")
            has_privacy = False
            has_tos = False
            detected_language = "error"
        
        browser.close()
        return "Y" if has_privacy else "N", "Y" if has_tos else "N", detected_language

def process_csv(input_file, output_file):
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        
        for row in reader:
            url = row.get("Website URL", "").strip()
            if url:
                privacy, tos, language = check_page_text(url)
                row["Privacy Policy"] = privacy
                row["Terms of Service"] = tos
                row["Language"] = language
            rows.append(row)
    
    with open(output_file, "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Website URL", "Privacy Policy", "Terms of Service", "Language"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

@app.route('/process_csv', methods=['POST'])
def process_csv_request():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    input_path = "uploaded.csv"
    output_path = "processed_output.csv"
    file.save(input_path)
    
    print("Starting CSV processing...")
    process_csv(input_path, output_path)
    print("CSV processing complete.")
    
    return send_from_directory('.', output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
