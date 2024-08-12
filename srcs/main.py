import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def fetch_rights(driver, title, artist):
    base_url = "https://repertoire.sacem.fr"
    driver.get(base_url)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idFullSearch")))
    search_field_title = driver.find_element(By.ID, 'idFullSearch')
    search_field_title.clear()
    search_field_title.send_keys(title)
    
    search_field_artist = driver.find_element(By.ID, 'idCreatorSearch')
    search_field_artist.clear()
    search_field_artist.send_keys(artist)
    
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "searchBtn"))
    )
    search_button.click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "section.meaResultats"))
    )

    # Cibler et cliquer sur le lien "voir le détail"
    voir_detail_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='btn univ right']/a"))
    )
    voir_detail_button.click()

    # Attendre et extraire les informations de la page de détails
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "grid2.borderBoxMod.mod"))
    )
    
    # Trouver tous les éléments <a> contenant les noms/prénoms
    names_elements = driver.find_elements(By.CSS_SELECTOR, "a.tooltip > span")

    # Extraire les noms et prénoms
    names = [element.text for element in names_elements]

    print("Noms et prénoms des ayants droit :")
    for name in names:
        print(name)
    
    return names

def generate_descriptions(csv_file, headless=True):
    driver = setup_driver(headless)
    data = pd.read_csv(csv_file)
    descriptions = []
    
    for index, row in data.iterrows():
        names = fetch_rights(driver, row['Titre'], row['Interprete'])
        description = f"Titre : {row['Titre']}, Interprète : {row['Interprete']}, Ayants droit : {', '.join(names)}"
        descriptions.append(description)
    
    driver.quit()
    return descriptions

# Exécuter la fonction et imprimer les résultats
descriptions = generate_descriptions('sample_sacem.csv', headless=False)
for desc in descriptions:
    print(desc)
