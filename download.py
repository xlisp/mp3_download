from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import wget

def download_mp3(song_name, download_folder="downloads"):
    """
    Downloads an MP3 from xmwav.com based on the song name.
    
    Args:
        song_name: The name of the song to search for
        download_folder: Folder to save the downloaded MP3
    """
    # Create download directory if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        
    # Setup Chrome options
    chrome_options = Options()
    prefs = {"download.default_directory": os.path.abspath(download_folder)}
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Step 1: Go to search page and input song name
        driver.get("https://www.xmwav.com/index/search/")
        
        # Wait for search input to load and enter song name
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "edtSearch"))
        )
        search_input.clear()
        search_input.send_keys(song_name)
        search_input.send_keys(Keys.RETURN)
        
        # Step 2: Wait for search results and click the first result
        result_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul li a[href^='/mscdetail/']"))
        )
        
        link_url = result_link.get_attribute("href")
        print(f"Found song link: {link_url}")
        result_link.click()
        
        # Step 3: On the detail page, find and click the "夸克MP3链接下载" button
        quark_download_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '夸克MP3链接下载')]"))
        )
        
        quark_download_btn.click()
        
        # Switch to the new tab (Quark pan page)
        driver.switch_to.window(driver.window_handles[-1])
        
        # Step 4: On the Quark pan page, find and click the download button
        download_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'download') or contains(text(), '下载')]"))
        )
        
        download_btn.click()
        
        # Wait for download to complete (this is a simple wait, could be improved)
        print("Waiting for download to complete...")
        time.sleep(10)
        
        print(f"Song '{song_name}' has been downloaded to {download_folder}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    song_name = input("Enter the name of the song to download: ")
    download_mp3(song_name)
