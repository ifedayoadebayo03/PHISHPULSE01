import base64
import requests
from playwright.sync_api import sync_playwright

print("[*] Screenshotting http://localhost:9999 ...")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("http://localhost:9999")
    screenshot = page.screenshot(type="png")
    browser.close()

b64_image = base64.b64encode(screenshot).decode('utf-8')
print(f"[*] Screenshot captured: {len(screenshot)} bytes -> base64: {len(b64_image)} chars")

print("[*] Sending to PhishPulse visual scanner...")
response = requests.post(
    "http://localhost:8000/api/v1/scan/",
    headers={"Content-Type": "application/json"},
    json={"type": "visual", "target": b64_image}
)

print(f"[*] Status: {response.status_code}")
data = response.json()
print(f"\n[RESULT] Scan ID: {data.get('scan_id')}")
print(f"[RESULT] Classification: {data.get('classification')}")
print(f"[RESULT] Final Score: {data.get('final_score')}")
print(f"[RESULT] Model Breakdown: {data.get('model_breakdown')}")
