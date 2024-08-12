import os
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

def fetch_rights(driver, title, artist, timeout=2):
    base_url = "https://repertoire.sacem.fr"
    driver.get(base_url)
    
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
    
    # Attendre que les résultats apparaissent, avec un délai maximum
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section.meaResultats"))
        )

        # Essayer de trouver et cliquer sur le bouton "voir le détail"
        voir_detail_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='btn univ right']/a"))
        )
        voir_detail_button.click()

        # Attendre que la page de détails soit chargée
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "grid2.borderBoxMod.mod"))
        )
        
        names_elements = driver.find_elements(By.CSS_SELECTOR, "a.tooltip > span")
        names = [element.text.strip() for element in names_elements if element.text.strip()]

        # Formater chaque nom pour capitaliser la première lettre de chaque mot
        formatted_names = [name.title() for name in names]
        return formatted_names
    except Exception as e:
        # Si le bouton "voir le détail" n'e`st` pas trouvé, retourner un message d'erreur
        print(f"Erreur lors de la recherche pour '{title} - {artist}': {str(e)}")
        return ["Aucun résultat trouvé pour cette recherche"]

def generate_descriptions(csv_file, headless=True):
    driver = setup_driver(headless)

    try:
        data = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        print(f"Erreur : Le fichier '{csv_file}' est vide.")
        return []

    if data.empty:
        print(f"Erreur : Le fichier '{csv_file}' est vide.")
        return []

    descriptions = []
    
    for index, row in data.iterrows():
        names = fetch_rights(driver, row['Titre'], row['Interprete'])
        description = f"{row['Titre']} - {row['Interprete']} ({', '.join(names)})"
        descriptions.append(description)
    
    driver.quit()
    return descriptions

def find_first_csv_in_input_folder():
    input_folder = 'input'
    if not os.path.exists(input_folder):
        print(f"Erreur : Le dossier '{input_folder}' n'existe pas.")
        return None

    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    if not csv_files:
        print(f"Erreur : Aucun fichier CSV trouvé dans le dossier '{input_folder}'.")
        return None

    return os.path.join(input_folder, csv_files[0])

def write_descriptions_to_file(descriptions, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for description in descriptions:
            f.write(description + '\n')

def main():
    csv_file = find_first_csv_in_input_folder()

    if not csv_file:
        print("Erreur : Aucun fichier CSV n'a été trouvé pour traitement.")
        return

    descriptions = generate_descriptions(csv_file, headless=False)

    if descriptions:
        output_file = 'output/descriptions.txt'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        write_descriptions_to_file(descriptions, output_file)
        print(f"Descriptions écrites dans le fichier : {output_file}")
    else:
        print("Aucune description à écrire.")

if __name__ == "__main__":
    main()
