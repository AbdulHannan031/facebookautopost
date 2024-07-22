import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
# Setup Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-data-dir=C:/Users/Toshiba/AppData/Local/Google/Chrome/User Data")  # Update this path
    chrome_options.add_argument("profile-directory=Profile 1")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Load Facebook cookies from JSON file
def load_facebook_cookies(driver, json_path):
    with open(json_path, 'r') as file:
        cookies_data = json.load(file)
        for cookie in cookies_data["cookies"]:
            # Fix the sameSite attribute
            if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                del cookie["sameSite"]
            driver.add_cookie(cookie)

# Extract group IDs from Excel file based on account
def extract_group_ids(excel_path, account_name):
    df = pd.read_excel(excel_path)
    if account_name in df.columns:
        return df[account_name].dropna().tolist()
    else:
        print(f"Account name {account_name} not found in {excel_path}")
        return []

# Process a single account and group ID pair
def process_account_and_group(driver, account_path, group_path, account_name):
    # Load Facebook cookies
    load_facebook_cookies(driver, account_path)

    # Extract group IDs
    group_ids = extract_group_ids(group_path, account_name)
    print(f"Extracted Group IDs for {account_name} from {os.path.basename(group_path)}: {group_ids}")
    return group_ids
def check_if_login_page(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
        return True
    except:
        return False
# Main function to automate the process
def main():
    # Define the base directory
    base_dir = 'Accounts'

    # Setup the WebDriver
    driver = setup_driver()

    # Navigate to Facebook
    # Iterate over all subfolders in the base directory
    for subfolder in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder)
        print(subfolder_path)
        if os.path.isdir(subfolder_path):
            group_ids_path = os.path.join(subfolder_path, 'groupids.xlsx')
            linnkpath = os.path.join(subfolder_path, 'Post.txt')

            if os.path.exists(linnkpath):
             with open(linnkpath, 'r') as file:
                linnk = file.read().strip() 
            print(group_ids_path)
            if os.path.exists(group_ids_path):
                for i in range(1, 31):  # Iterate from 1 to 30
                    account_file = f"Acc ({i}).json"
                    account_path = os.path.join(subfolder_path, account_file)
                    if os.path.exists(account_path):
                        if account_file=="Acc 1.json" or account_file=="Acc 2.json" or account_file=="Acc 3.json":
                            continue
                        driver.get('https://www.facebook.com')
                        driver.delete_all_cookies()
                        print(f"Processing {account_file}")
                        account_name = os.path.splitext(account_file)[0]
                        group_ids = process_account_and_group(driver, account_path, group_ids_path, account_name)
                        driver.refresh()  # Allow time for cookies to take effect
                        time.sleep(5)
                        try:
                          # Wait for the span element containing the specific text to be visible
                          element = WebDriverWait(driver, 10).until(
                              EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'your account has been locked')]"))
                          )
                          if element:
                              with open(os.path.join(subfolder_path, 'dead.txt'), 'a') as dead_file:
                                  dead_file.write(f"{account_file}\n")
                              print(f"{account_file} marked as dead.")
                              continue
                        except Exception:
                            print("Account is alright")

                        if check_if_login_page(driver):

                            with open(os.path.join(subfolder_path, 'dead.txt'), 'a') as dead_file:
                                dead_file.write(f"{account_file}\n")
                            
                            print(f"{account_file} marked as dead.")
                            continue
                        driver.get('https://v2.fewfeed.com/tool/v3-groups-share')
                        time.sleep(5)
                        driver.refresh()
                        text1=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/div[2]/div/div/div/div[1]/div[3]/input')))
                        text1.clear()
                        text1.send_keys('1')
                        uncheck=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/div[2]/div/div/div/div[3]/div[1]/div/div/div[1]/input')))
                        uncheck.click()
                        linktex=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/div[2]/div/div/div/div[3]/div[2]/input')))
                        linktex.clear()
                        linktex.send_keys(linnk)
                        time.sleep(3)
                        area=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/div[2]/div/div/div/div[3]/div[4]/textarea')))
                        area.clear()
                        for ids in group_ids:
                            area.send_keys(ids,'\n')
                        time.sleep(3)
                        
                        but=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/div[2]/div/div/div/div[1]/button')))
                        but.click()
                        time.sleep(200)                      

                    else:
                        print(f"{account_file} not found, skipping.")

            else:
                print(f"groupids.xlsx not found in {subfolder}")

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()
