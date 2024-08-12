import os

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