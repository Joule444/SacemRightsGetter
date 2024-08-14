import os
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def fetch_rights(driver, title, artist, timeout=2):
    base_url = "https://repertoire.sacem.fr"
    driver.get(base_url)
    
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "idFullSearch")))
        search_field_title = driver.find_element(By.ID, 'idFullSearch')
        search_field_title.clear()
        search_field_title.send_keys(title)
        
        search_field_artist = driver.find_element(By.ID, 'idCreatorSearch')
        search_field_artist.clear()
        search_field_artist.send_keys(artist)
        
        search_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "searchBtn"))
        )
        search_button.click()
        
        screenshot_dir = 'screenshots'
        ensure_directory_exists(screenshot_dir)
        
        # Capture d'écran après l'envoi du formulaire
        screenshot_path = os.path.join(screenshot_dir, f"screenshot_{title}_{artist}.png")
        driver.save_screenshot(screenshot_path)
        
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section.meaResultats"))
        )

        voir_detail_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='btn univ right']/a"))
        )
        voir_detail_button.click()

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "grid2.borderBoxMod.mod"))
        )
        
        names_elements = driver.find_elements(By.CSS_SELECTOR, "a.tooltip > span")
        names = [element.text.strip() for element in names_elements if element.text.strip()]
        formatted_names = [name.title() for name in names]
        return formatted_names
    
    # Capturer des exceptions spécifiques pour éviter les stacktraces
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error searching for '{title} - {artist}': Element not found or timed out.")
        return ["No results found for this search"]
    
    except Exception as e:
        print(f"An unexpected error occurred while searching for '{title} - {artist}': {str(e)}")
        return ["No results found due to an unexpected error"]

def generate_descriptions(csv_file, headless=True):
    driver = setup_driver(headless)

    try:
        data = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_file}' is empty.")
        return []

    if data.empty:
        print(f"Error: The file '{csv_file}' is empty.")
        return []

    descriptions = []
    
    for index, row in data.iterrows():
        title = row['Title'] if pd.notna(row['Title']) else ""
        artist = row['Artist'] if pd.notna(row['Artist']) else ""
        names = fetch_rights(driver, title, artist)
        description = f"\"{title}\" - {artist} ({', '.join(names)})"
        descriptions.append(description)
    
    driver.quit()
    return descriptions
