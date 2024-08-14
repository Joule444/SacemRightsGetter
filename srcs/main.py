import sys
import os
from selenium.webdriver.common.keys import Keys
from parsing import find_first_csv_in_input_folder
from process import generate_descriptions
from writing_output import write_descriptions_to_file

def main(headless=True):
    csv_file = find_first_csv_in_input_folder()

    descriptions = generate_descriptions(csv_file, headless=headless)

    if descriptions:
        output_file = 'output/descriptions.txt'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        write_descriptions_to_file(descriptions, output_file)
        print(f"Description written in the file : {output_file}")
    else:
        print("No description to write.")

if __name__ == "__main__":
    headless = True
    if len(sys.argv) > 1 and sys.argv[1].lower() == "noheadless":
        headless = False

    main(headless=headless)
