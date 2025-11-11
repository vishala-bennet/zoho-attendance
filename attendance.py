import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


class ZohoPeopleAttendanceAgent:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
        # ✅ FIXED: Add headless mode for GitHub Actions
        options = Options()
        options.add_argument("--headless")  # No display window
        options.add_argument("--no-sandbox")  # For GitHub Actions
        options.add_argument("--disable-dev-shm-usage")  # For GitHub Actions
        options.add_argument("--disable-gpu")  # No GPU needed
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 15)
    
    def login_and_checkin(self):
        try:
            print("🔄 Starting Zoho People automation...")
            
            # Step 1: Navigate to Zoho People
            self.driver.get("https://people.zoho.in/customerlabs/zp#home/myspace/overview-actionlist")
            print("✓ Navigated to Zoho People")
            time.sleep(3)
            
            # Step 2: Fill email field
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "login_id"))
            )
            email_field.clear()
            email_field.send_keys(self.email)
            print(f"✓ Entered email: {self.email}")
            time.sleep(1)
            
            # Step 3: Click Next button
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='nextbtn']"))
            )
            next_button.click()
            print("✓ Clicked Next")
            time.sleep(2)
            
            # Step 4: Fill password field
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_field.clear()
            password_field.send_keys(self.password)
            print("✓ Entered password")
            time.sleep(1)
            
            # Step 5: Click Sign in button
            signin_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='nextbtn']"))
            )
            signin_button.click()
            print("✓ Clicked Sign in")
            time.sleep(4)
            
            # Step 6: Click Check-in/Check-out button
            checkin_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='ZPAtt_check_in_out']"))
            )
            checkin_button.click()
            print("✓ Clicked Check-in/Check-out")
            time.sleep(2)
            
            print("✅ Success! Attendance marked!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()  # Print full error details
        
        finally:
            time.sleep(3)
            self.driver.quit()


# Usage
if __name__ == "__main__":
    # ✅ FIXED: Read from environment variables (GitHub Secrets)
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    
    if not email or not password:
        print("❌ EMAIL or PASSWORD not set in environment variables")
        exit(1)
    
    print(f"📧 Running with email: {email}")
    agent = ZohoPeopleAttendanceAgent(email, password)
    agent.login_and_checkin()
