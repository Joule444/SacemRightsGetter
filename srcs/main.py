import time
import os
from selenium.webdriver.common.keys import Keys
from parsing import find_first_csv_in_input_folder
from process import generate_descriptions
from writing_output import write_descriptions_to_file

def main():
    csv_file = find_first_csv_in_input_folder()

    if not csv_file:
        print("Erreur : Aucun fichier CSV n'a été trouvé pour traitement.")
        return

    descriptions = generate_descriptions(csv_file, headless=True)

    if descriptions:
        output_file = 'output/descriptions.txt'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        write_descriptions_to_file(descriptions, output_file)
        print(f"Descriptions écrites dans le fichier : {output_file}")
    else:
        print("Aucune description à écrire.")

if __name__ == "__main__":
    main()
