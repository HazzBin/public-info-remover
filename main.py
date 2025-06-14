from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import time

# Start Chrome
service = Service()
driver = webdriver.Chrome(service=service)
driver.set_window_position(-2000, 0)

personalEmail = input("Enter your personal email and press enter: ")

# Tasks to be completed
tasks = [
    {
        "name": "ClustrMaps",
        "url": input("\nLet's begin with ClustrMaps:\n 1. Navigate to https://clustrmaps.com/\n 2. Find your public profile\n 3. Paste the profile link below\n 4. Press Enter\n\n").strip(),
        "steps": [
            {
                "by": By.ID,
                "value": "opt-out",
                "action": "click",
                "data": "",
                "special": "submit_in_form_with_span"
            },
            {
                "by": By.NAME,
                "value": "inputEmail",
                "action": "send_keys",
                "data": personalEmail,
                "check_captcha": True
            },
            {
                "by": By.XPATH,
                "value": "//button[@type='submit']",
                "action": "click"
            },
            {
                "by": By.CSS_SELECTOR,
                "value": "input[type='checkbox'][name='phones[]']",
                "action": "check_all"
            },
            {
                "by": By.CSS_SELECTOR,
                "value": "input[type='checkbox'][name='persons[]']",
                "action": "check_all"
            },
            {
                "by": By.CSS_SELECTOR,
                "value": "input[type='checkbox'][name='parcels[]']",
                "action": "check_all"
            },
                        {
                "by": By.CSS_SELECTOR,
                "value": "input.btn.btn-primary.mt-3.pl-3.pr-3",
                "action": "click",
                "end": True
            }
        ]
    },
'''
    {
        "name": "Spy Dialer",
        "url": "https://www.spydialer.com/optout",
        "steps": [
            {
                "by": By.ID,
                "value": "name",
                "action": "send_keys",
                "data": "Michael Catelli"
            },
            {
                "by": By.ID,
                "value": "email",
                "action": "send_keys",
                "data": "your@email.com"
            }
        ],
        "requires_captcha": False
    }
    '''
]

def bring_browser_to_front():
    # MacOS
    driver.set_window_position(0, 0)
    subprocess.run([
        "osascript", "-e",
        'tell application "Google Chrome" to activate'
    ])


def perform_action(elem, action, data, step=None):
    if action == "click":
        if step and step.get("special") == "submit_in_form_with_span":
            try:
                form = elem.find_element(By.XPATH, "./ancestor::form")
                submit_button = form.find_element(By.CSS_SELECTOR, "input[type='submit']")
                submit_button.click()
            except Exception as e:
                print(f" - Failed to find or click submit button inside form: {e}")
        else:
            elem.click()
    elif action == "check_all":
        try:
            elems = driver.find_elements(step["by"], step["value"])
            for checkbox in elems:
                if not checkbox.is_selected():
                    checkbox.click()
        except Exception as e:
            print(f" - Failed to check all checkboxes for {step['value']}: {e}")
    else:
        getattr(elem, action)(data)

def check_for_captcha():
    print(" - Checking for CAPTCHA iframe...")
    captcha_iframes = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
    if captcha_iframes:
        print(" - CAPTCHA detected! Bringing browser to front.")
        bring_browser_to_front()
        input(" * Solve CAPTCHA manually, then press Enter to continue...")
        driver.set_window_position(-2000, 0)



def process_task(task):
    print(f"\n▶️ Starting: {task['name']}")
    driver.get(task["url"])
    time.sleep(2)

    for step in task["steps"]:
        try:
            if step["action"] == "check_all":
                # Handle multiple checkboxes directly
                elems = driver.find_elements(step["by"], step["value"])
                if not elems:
                    continue
                for checkbox in elems:
                    if not checkbox.is_selected():
                        checkbox.click()
                continue 
            
            # Default / One element
            elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((step["by"], step["value"]))
            )
            perform_action(elem, step["action"], step.get("data", ""), step=step)

            if step.get("check_captcha"):
                check_for_captcha()

            if step.get("end"):
                print(" * Personal information successfully removed!")
                break

        except Exception as e:
            print(f" - Failed to perform {step['action']} on {step['value']}: {e}")


# Run tasks
for task in tasks:
    process_task(task)

print(" - All tasks complete. Exiting...")
driver.quit()