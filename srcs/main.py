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
    
    # Assure-toi que les éléments sont présents
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idFullSearch")))
    search_field_title = driver.find_element(By.ID, 'idFullSearch')
    search_field_title.clear()
    search_field_title.send_keys(title)
    
    search_field_artist = driver.find_element(By.ID, 'idCreatorSearch')
    search_field_artist.clear()
    search_field_artist.send_keys(artist)
    
    # Trouver le bouton de recherche et cliquer dessus
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "searchBtn"))
    )
    search_button.click()
    
    # Attendre que la page avec les résultats se charge
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "selecteur_css_pour_les_resultats"))
    )
    
    # Extraction et affichage des résultats (adapter selon le site)
    results_info = driver.find_element(By.CSS_SELECTOR, 'selecteur_css_pour_les_infos').text
    print("Résultats trouvés :", results_info)

def generate_descriptions(csv_file, headless=True):
    driver = setup_driver(headless)
    data = pd.read_csv(csv_file)
    descriptions = []
    
    for index, row in data.iterrows():
        fetch_rights(driver, row['Titre'], row['Interprete'])
    
    driver.quit()
    return descriptions

# Exécuter la fonction et imprimer les résultats
descriptions = generate_descriptions('sample_sacem.csv', headless=False)
for desc in descriptions:
    print(desc)
