'''
# Web Browser Automation with Selenium

This script uses Selenium to programmatically control a web browser. It opens Google, performs a search, waits for the results to load, and then scrapes the titles of the top search results. This is useful for testing web applications or scraping data from dynamic JavaScript-heavy websites.

Concepts: 

Browser automation, web scraping, controlling web drivers.

**How to Run**

**1. Save the code and execute it:**

```
python Program_10.py
```
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def perform_google_search(query):
    """
    Automates a Google search and prints the titles of the top results.
    """
    # Automatically download and manage the correct ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # 1. Open Google
        driver.get("https://www.google.com")
        print("Opened Google.com")

        # 2. Find the search box element
        # The element name can change; inspect the page to find the current one (e.g., 'q')
        search_box = driver.find_element(By.NAME, "q")

        # 3. Type the search query and press Enter
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        print(f"Performing search for: '{query}'")

        # 4. Wait for results to load
        time.sleep(3) # A simple wait; for robust scripts, use WebDriverWait

        # 5. Find all result titles (typically in <h3> tags)
        print("\n--- Top Search Results ---")
        results = driver.find_elements(By.TAG_NAME, "h3")
        
        if not results:
            print("Could not find any results.")
        
        for i, result in enumerate(results[:5]): # Print top 5
            print(f"{i+1}. {result.text}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # 6. Close the browser
        driver.quit()
        print("\nBrowser closed.")

if __name__ == "__main__":
    search_query = "The future of artificial intelligence"
    perform_google_search(search_query)