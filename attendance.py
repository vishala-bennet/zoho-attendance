import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import traceback


class ZohoPeopleAttendanceAgent:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-resources")
        options.add_argument("--disable-extensions")
        
        print(f"🔧 Initializing Chrome...")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 20)  # Increased timeout
    
    def login_and_checkin(self):
        try:
            print("🔄 Starting Zoho People automation...")
            print(f"📧 Email: {self.email}")
            
            # Step 1: Navigate to Zoho People
            print("📍 [Step 1] Navigating to Zoho People...")
            self.driver.get("https://people.zoho.in/customerlabs/zp#home/myspace/overview-actionlist")
            print("✓ Page loaded, waiting for email field...")
            time.sleep(5)
            
            # Step 2: Fill email field
            print("📍 [Step 2] Filling email field...")
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "login_id")),
                message="Email field not found!"
            )
            email_field.clear()
            email_field.send_keys(self.email)
            print(f"✓ Email entered: {self.email}")
            time.sleep(1)
            
            # Step 3: Click Next button
            print("📍 [Step 3] Clicking Next button...")
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='nextbtn']")),
                message="Next button not found!"
            )
            next_button.click()
            print("✓ Clicked Next")
            time.sleep(3)
            
            # Step 4: Fill password field
            print("📍 [Step 4] Filling password field...")
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "password")),
                message="Password field not found!"
            )
            password_field.clear()
            password_field.send_keys(self.password)
            print("✓ Password entered")
            time.sleep(1)
            
            # Step 5: Click Sign in button
            print("📍 [Step 5] Clicking Sign in button...")
            signin_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='nextbtn']")),
                message="Sign in button not found!"
            )
            signin_button.click()
            print("✓ Clicked Sign in")
            time.sleep(5)
            
            # Step 6: Click Check-in/Check-out button
            print("📍 [Step 6] Clicking Check-in/Check-out button...")
            checkin_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='ZPAtt_check_in_out']")),
                message="Check-in button not found!"
            )
            checkin_button.click()
            print("✓ Clicked Check-in/Check-out")
            time.sleep(3)
            
            print("✅ SUCCESS! Attendance marked!")
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR OCCURRED:")
            print(f"Error message: {str(e)}")
            print(f"\nFull traceback:")
            traceback.print_exc()
            print(f"\n🔍 Current page URL: {self.driver.current_url}")
            print(f"🔍 Page title: {self.driver.title}")
            return False
        
        finally:
            try:
                # Take a screenshot for debugging
                self.driver.save_screenshot("debug_screenshot.png")
                print("\n📸 Debug screenshot saved!")
            except:
                pass
            
            time.sleep(2)
            self.driver.quit()
            print("Browser closed.")


# Usage
if __name__ == "__main__":
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    
    if not email or not password:
        print("❌ ERROR: EMAIL or PASSWORD not set!")
        print("Make sure you added ZOHO_EMAIL and ZOHO_PASSWORD secrets to GitHub")
        exit(1)
    
    print("=" * 50)
    print("🚀 ZOHO ATTENDANCE AUTOMATION")
    print("=" * 50)
    
    agent = ZohoPeopleAttendanceAgent(email, password)
    success = agent.login_and_checkin()
    
    if success:
        print("\n🎉 Workflow completed successfully!")
        exit(0)
    else:
        print("\n⚠️ Workflow completed but automation failed!")
        exit(1)
