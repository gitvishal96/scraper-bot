from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import os
import undetected_chromedriver as uc

# options = Options()
# options.headless = True  

# Specify the path to Chromedriver if it's not on PATH
webdriver_service = Service(executable_path='/path/to/chromedriver')  # Replace with your driver path, if not on PATH
webdriver_service = uc.Chrome(headless=True)
url = " "

def scrape_with_retry(url, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            # driver = webdriver.Chrome(service=webdriver_service)
            driver = uc.Chrome(headless=True)
            driver.get(url)
            time.sleep(3)  # Wait for JavaScript to load

            # Extract the text content from all the <p> tags on the page
            paragraphs = driver.find_elements(By.TAG_NAME, 'p')
            text = '\n'.join([paragraph.text for paragraph in paragraphs])

            # Save the text content to a .txt file
            with open('output.txt', 'w', encoding='utf-8') as file:
                file.write(text)

            driver.quit()  # Close the browser
            return True
        except WebDriverException as e:
            print(f"Error occurred: {e}")
            attempts += 1
            time.sleep(2 ** attempts)  # Exponential backoff
        finally:
            if 'driver' in locals():
                driver.quit()  # Ensure the driver is closed if an exception is raised

    return False  # Indicate failure after all attempts

successful = scrape_with_retry(url)
if successful:
    print("Scraping succeeded")
else:
    print("Scraping failed after all retries")